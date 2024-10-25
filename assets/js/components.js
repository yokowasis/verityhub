/** @type {import("../../types").WInput} */
const w = /** @type {*} */ (window);

class Profile extends HTMLElement {
  connectedCallback() {
    this.render();
  }

  async render() {
    /** @type {import("../../types").DBClient} */
    const db = /** @type {*} */ (window).db;
    const user = await getUser();

    if (!user?.id) return;

    const { data, error } = await db
      .from("users")
      .select("*")
      .eq("user_id", user.id);

    this.innerHTML = /*html*/ `
        <div class="profile">
          <div class="profile-image">
            <img src="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
              alt="Profile Picture">
          </div>
          <div class="profile-identity">
            <div class="profile-name">
              ${data?.[0].full_name}
            </div>
            <div class="profile-handle">
              @${data?.[0].handler}
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
      return;
    }

    this.innerHTML = /*html*/ `
        <p class="fs-08">Login to follow profiles or hashtags, favourite, share and reply to posts. You can also interact from your account on a different server.</p>
        <div>
          <input type="text" class="form-control mb-3" placeholder="Username" id="username" />
          <input type="password" class="form-control mb-3" placeholder="Password" id="password" />
          <input type="password" class="form-control mb-3" placeholder="Confirm Password" id="confirm-password" />
          <input type="text" class="form-control mb-3" placeholder="User Handler" id="userhandler" />
          <input type="text" class="form-control mb-3" placeholder="Full Name" id="fullname" />
          <button type="button" id="signin-btn" class="btn btn-block btn-primary">Sign in</button>
          <button type="button" id="create-account-btn" class="btn btn-block btn-link">Create Account</button>
        </div>
      `;

    const signinBtn = document.getElementById("signin-btn");

    if (signinBtn) {
      signinBtn.addEventListener("click", () => {
        w.toast.loading("Please Wait ...");

        const username = w.getVal("username");
        const password = w.getVal("password");

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
