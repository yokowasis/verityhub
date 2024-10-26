/** @type {import("../../types").DBClient} */
const db = /** @type {*} */ (window).base;

/** @type {import("../../types").WInput} */
const w = /** @type {*} */ (window);

async function isAuth() {
  const user = await db?.auth?.getUser();

  if (user?.data?.user) {
    return true;
  } else {
    return false;
  }
}

async function getUser() {
  const user = (await db.auth.getUser()).data.user;
  return user;
}

async function getUserBio() {
  const user = await getUser();

  if (!user) {
    return;
  }

  const { data, error } = await db
    .from("users")
    .select("*")
    .eq("user_id", user.id);

  if (error) {
    return;
    console.log(error);
  }

  const bio = data[0];
  return bio;
}

/**
 *
 * @param {string} s
 */
async function getSummary(s) {
  /** @type {string} */
  const r = await (
    await fetch(`https://nlp.backend.b.app.web.id/api/summarize`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: s,
      }),
    })
  ).json();

  return r;
}

/**
 *
 * @param {string} text
 */
async function getVector(text) {
  /** @type {number[]} */
  const r = await (
    await fetch(`https://nlp.backend.b.app.web.id/api/vectorize`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text,
      }),
    })
  ).json();

  return r;
}

async function logout() {
  w.toast.loading("Please Wait ...");
  const promises = [];

  promises.push(db.auth.signOut());
  promises.push(
    fetch(`/logout`, {
      method: "GET",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    })
  );

  await Promise.all(promises);

  w.location.reload();
}

/**
 *
 * @param {string} username
 * @param {string} password
 */
async function signIn(username, password) {
  w.toast.loading("Please Wait ...");

  const promises = [];

  promises.push(
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
  );

  promises.push(
    db.auth.signInWithPassword({
      email: `${username}@verityhub.id`,
      password: password,
    })
  );

  Promise.allSettled(promises)
    .then((res) => {
      /** @type {*[]} */
      const s = /** @type {*} */ (res);
      if (s?.[1]?.value?.error?.message) {
        w.toast.error("Login Failed !");
      } else {
        w.toast.success("Login Success !");
        w.location.reload();
      }
    })
    .catch(() => {
      w.toast.error("Login Failed !");
    });
}

/**
 *
 * @param {string} username
 * @param {string} password
 * @param {string} confirmPassword
 * @param {string} userhandler
 * @param {string} fullname
 * @param {string} avatar
 */
async function createAccount(
  username,
  password,
  confirmPassword,
  userhandler,
  fullname,
  avatar
) {
  w.toast.loading("Please Wait ...");

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
    avatar: avatar,
  });

  if (doUpsert.error) {
    w.toast.error(doUpsert.error.message);
    return;
  }

  w.toast.success(
    "Account Created ! You can now login using your new account."
  );
}
