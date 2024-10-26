/** @type {import("../../types.ts").WInput} */
const w = /** @type {*} */ (window);

async function logout() {
  w.toast.loading("Please Wait ...");
  const promises = [];

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
  const r = await (
    await fetch(`/login`, {
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
  ).json();

  const message = r.message;
  if (message === "Login Success !") {
    w.toast.success("Login Success !");
    w.location.reload();
  } else {
    w.toast.error("Login Failed !");
  }
}

/**
 *
 * @param {string} username
 * @param {string} password
 * @param {string} confirmPassword
 * @param {string} full_name
 * @param {string} avatar
 */
async function signUp(username, password, confirmPassword, full_name, avatar) {
  w.toast.loading("Please Wait ...");

  // make sure confirm password is the same as password
  if (password !== confirmPassword) {
    return {
      message: "Passwords do not match !",
    };
  }

  // make sure everything is filled
  if (!username || !password || !confirmPassword || !full_name || !avatar) {
    return {
      message: "Please fill all fields !",
    };
  }

  console.log({
    username,
    password,
    confirmPassword,
    full_name,
    avatar,
  });

  const r = await (
    await fetch(`/signup`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
        avatar,
        full_name,
      }),
    })
  ).json();

  return r;
}

async function post(content) {
  const r = await (
    await fetch(`/post`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        content,
      }),
    })
  ).json();

  return r;
}
