/** @type {import("@supabase/supabase-js").SupabaseClient} */
const db = /** @type {*} */ (window).db;

/** @type {import("../../types").WInput} */
const w = /** @type {*} */ (window);

async function isAuth() {
  const user = await db?.auth?.getUser();

  if (user.data?.user) {
    return true;
  } else {
    return false;
  }
}

const createAccountBtn = document.getElementById("create-account-btn");

if (createAccountBtn) {
  createAccountBtn.addEventListener("click", async () => {
    w.toast.loading("Please Wait ...");

    const username = w.getVal("username");
    const password = w.getVal("value");
    const confirmPassword = w.getVal("confirm-password");
    const userhandler = w.getVal("userhandler");
    const fullname = w.getVal("fullname");

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
  });
}
