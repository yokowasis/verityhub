/** @type {*} */
(window).db =
  /** @type {*} */
  (window).supabase.createClient(
    "http://localhost:8000",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ewogICJyb2xlIjogImFub24iLAogICJpc3MiOiAic3VwYWJhc2UiLAogICJpYXQiOiAxNzI5NDQwMDAwLAogICJleHAiOiAxODg3MjA2NDAwCn0.XSQrv4DZV9WXfTysRQZAp0FJoLdPrTXptdk0qgXIW0A"
  );

class Profile extends HTMLElement {
  connectedCallback() {
    this.render();
  }

  render() {
    this.innerHTML = /*html*/ `
        <div class="profile">
          <div class="profile-image">
            <img src="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
              alt="Profile Picture">
          </div>
          <div class="profile-identity">
            <div class="profile-name">
              John Doe
            </div>
            <div class="profile-handle">
              @johndoe
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

  render() {
    this.innerHTML = /*html*/ `
        <p class="fs-08">Login to follow profiles or hashtags, favourite, share and reply to posts. You can also interact from your account on a different server.</p>
        <div>
          <input type="text" class="form-control mb-3" placeholder="Username" id="username" />
          <input type="password" class="form-control mb-3" placeholder="Password" id="password" />
          <input type="text" class="form-control mb-3" placeholder="User Handler" id="userhandler" />
          <input type="text" class="form-control mb-3" placeholder="Full Name" id="fullname" />
          <button type="button" id="signin-btn" class="btn btn-block btn-primary">Sign in</button>
          <button type="button" id="create-account-btn" class="btn btn-block btn-link">Create Account</button>
        </div>
      `;

    const signinBtn = document.getElementById("signin-btn");
    const createAccountBtn = document.getElementById("create-account-btn");

    if (createAccountBtn) {
      createAccountBtn.addEventListener("click", () => {
        /** @type {import("../../types").WInput} */
        const w = /** @type {*} */ (window);

        w.toast.loading("Please Wait ...");

        const username =
          /** @type {HTMLInputElement} */
          (document.getElementById("username")).value;
        const password =
          /** @type {HTMLInputElement} */
          (document.getElementById("password")).value;
        const userhandler =
          /** @type {HTMLInputElement} */
          (document.getElementById("userhandler")).value;
        const fullname =
          /** @type {HTMLInputElement} */
          (document.getElementById("fullname")).value;

        /** @type {import("@supabase/supabase-js").SupabaseClient<import("../../supabase").Database>} */
        const db = /** @type {*} */ (window).db;

        // check if userhandler is available
        db.from("users")
          .select("handler")
          .eq("handler", userhandler)
          .limit(1)
          .single()
          .then((s) => {
            console.log(s);
            if (s.data) {
              return {
                data: [],
                error: {
                  message: "User Handler Already Exists !",
                },
              };
            } else {
              return;
            }
          })
          .then(async (s) => {
            if (s?.error) return s;
            return db.auth.signUp({
              email: `${username}@verityhub.id`,
              password: password,
            });
          })
          .then(async (s) => {
            if (s.error) {
              return s;
            } else {
              const userid = s.data.session?.user.id;
              if (userid) {
                return db.from("users").upsert({
                  user_id: userid,
                  full_name: fullname,
                  handler: userhandler,
                });
              } else {
                return s;
              }
            }
          })
          .then((s) => {
            if (s) {
              if (s.error) {
                w.toast.error(s.error.message);
              } else {
                w.toast.success("Account Created !");
              }
            } else {
              w.toast.error("Session not found");
            }
          });
      });
    }

    if (signinBtn) {
      signinBtn.addEventListener("click", () => {
        /** @type {import("../../types").WInput} */
        const w = /** @type {*} */ (window);

        w.toast.loading("Please Wait ...");

        const username =
          /** @type {HTMLInputElement} */
          (document.getElementById("username")).value;
        const password =
          /** @type {HTMLInputElement} */
          (document.getElementById("password")).value;

        /** @type {import("@supabase/supabase-js").SupabaseClient} */
        const db = /** @type {*} */ (window).db;

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
    }
  }
}

customElements.define("v-loginbox", LoginBox);
