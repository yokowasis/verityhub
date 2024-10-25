/** @type {import("../../types").WInput} */
const w = /** @type {*} */ (window);

class Profile extends HTMLElement {
  constructor() {
    super();
  }

  static get observedAttributes() {
    return ["handler"];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (name === "handler") {
      this.render();
    }
  }

  connectedCallback() {
    this.render();
  }

  async render() {
    const fullName = this.getAttribute("fullname");
    const handler = this.getAttribute("handler");
    const avatar = this.getAttribute("avatar");

    if (!fullName || !handler || !avatar) {
      console.log("Attributes Missing : fullname, handler");
      return;
    }

    this.innerHTML = /*html*/ `
        <div class="profile">
          <div class="profile-image">
            <img src="${
              avatar ||
              "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
            }"
              alt="Profile Picture">
          </div>
          <div class="profile-identity">
            <div class="profile-name">
              ${fullName}
            </div>
            <div class="profile-handle">
              @${handler}
            </div>
          </div>
        </div>
    `;
  }
}

customElements.define("v-profile", Profile);

class Sidebar extends HTMLElement {
  connectedCallback() {
    this.render();
  }

  render() {
    this.innerHTML = /*html*/ `

    `;
  }
}

customElements.define("v-sidebar", Sidebar);

class LoginBox extends HTMLElement {
  connectedCallback() {
    this.render();
  }

  async render() {
    /** @type {import("../../types").DBClient} */
    const db = /** @type {*} */ (window).db;

    if (await isAuth()) {
      this.innerHTML = /*html*/ `
        <button type="button" class="btn btn-block btn-primary" id="logout"><i class="fas fa-sign-out-alt"></i>
          Logout</button>
      `;
    } else {
      this.innerHTML = /*html*/ `
        <p class="fs-08">Login to follow profiles or hashtags, favourite, share and reply to posts. You can also interact from your account on a different server.</p>
        <div>
          <input type="text" class="form-control mb-3" placeholder="Username" id="userlogin" />
          <input type="password" class="form-control mb-3" placeholder="Password" id="passwordlogin" />
          <button type="button" id="signin-btn" class="btn btn-block btn-primary">Sign in</button>
        </div>
        <p class="text-center mt-3">- OR -</p>
        <div>
          <input type="text" class="form-control mb-3" placeholder="Username" id="username" />
          <input type="password" class="form-control mb-3" placeholder="Password" id="password" />
          <input type="password" class="form-control mb-3" placeholder="Confirm Password" id="confirm-password" />
          <input type="text" class="form-control mb-3" placeholder="User Handler" id="userhandler" />
          <input type="text" class="form-control mb-3" placeholder="Full Name" id="fullname" />
          <button type="button" id="create-account-btn" class="btn btn-block btn-danger">Create Account</button>
        </div>
      `;
    }

    const logoutBtn = document.getElementById("logout");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", async () => {
        w.toast.loading("Please Wait ...");
        await db.auth.signOut();
        w.location.reload();
      });
    }

    const signinBtn = document.getElementById("signin-btn");

    if (signinBtn) {
      signinBtn.addEventListener("click", () => {
        w.toast.loading("Please Wait ...");

        const username = w.getVal("userlogin");
        const password = w.getVal("passwordlogin");

        fetch("/login", {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username,
            password,
          }),
        })
          .then((res) => res.json())
          .then((result) => {
            console.log(result);
          })
          .catch((err) => {
            console.log(err);
          });

        db.auth
          .signInWithPassword({
            email: `${username}@verityhub.id`,
            password: password,
          })
          .then((s) => {
            if (s.error) {
              w.toast.error("Login Failed !");
            } else {
              w.toast.success("Login Success !");
              w.location.reload();
            }
          });
      });

      const createAccountBtn = document.getElementById("create-account-btn");

      if (createAccountBtn) {
        createAccountBtn.addEventListener("click", async () => {
          w.toast.loading("Please Wait ...");

          const username = w.getVal("username");
          const password = w.getVal("password");
          const confirmPassword = w.getVal("confirm-password");
          const userhandler = w.getVal("userhandler");
          const fullname = w.getVal("fullname");

          console.log({
            username,
            password,
            confirmPassword,
            userhandler,
            fullname,
          });

          // make sure confirm password is the same as password
          if (password !== confirmPassword) {
            w.toast.error("Passwords do not match !");
            return;
          }

          // check if userhandler is available
          const isAvailable = await db
            .from("users")
            .select("handler")
            .eq("handler", userhandler)
            .limit(1)
            .single();

          if (isAvailable.data) {
            w.toast.error("User Handler Already Exists !");
            return;
          }

          const doSignup = await db.auth.signUp({
            email: `${username}@verityhub.id`,
            password: password,
          });

          if (doSignup.error) {
            w.toast.error(doSignup.error.message);
            return;
          }

          const userid = doSignup.data.session?.user.id;

          if (!userid) {
            w.toast.error("User ID is not available !");
            return;
          }

          const doUpsert = await db.from("users").upsert({
            user_id: userid,
            full_name: fullname,
            handler: userhandler,
          });

          if (doUpsert.error) {
            w.toast.error(doUpsert.error.message);
            return;
          }

          w.toast.success("Account Created !");
          w.location.reload();
        });
      }
    }
  }
}

customElements.define("v-loginbox", LoginBox);

class Logo extends HTMLElement {
  connectedCallback() {
    this.render();
  }

  render() {
    this.innerHTML = /*html*/ `
      <h1 style="font-size: 2rem;" class="text-center">
        <img style="height: 50px;" src="/assets/images/logo-removebg-preview.png" />
        Verity<span style="color: #03a9f4;">Hub</span>
      </h1>    
    `;
  }
}

customElements.define("v-logo", Logo);
