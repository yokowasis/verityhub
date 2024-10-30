// @ts-check

// deno-lint-ignore-file no-unused-vars
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

/**
 *
 * @param {string} content
 * @param {"post" | "article" | "comment"} type
 * @param {string} parent
 * @returns
 */
async function post(content, type = "post", parent = "") {
  const r = await (
    await fetch(`/post`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        posttype: type,
        parent,
        content,
      }),
    })
  ).json();

  return r;
}

/**
 *
 * @param {string} post_id
 */
async function reply(post_id) {
  const contentDiv =
    /** @type {HTMLInputElement | null} */
    (document.getElementById(`reply-${post_id}`));
  if (!contentDiv) return;
  const content = contentDiv.value;
  const r = await (
    await fetch(`/reply`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        post_id,
        content,
      }),
    })
  ).json();

  return r;
}

/**
 *
 * @param {number} post_id
 * @returns
 */
function addReply(post_id) {
  console.log(post_id);
  const postDiv = document.getElementById(`post-${post_id}`);
  const replyBoxDiv = document.getElementById(`reply-box-${post_id}`);

  if (!postDiv || !replyBoxDiv) {
    console.log(postDiv);
    console.log(replyBoxDiv);
    return;
  }

  replyBoxDiv.innerHTML = /*html*/ `
  <v-postbox
    id="newpost-${post_id}"
    type="comment"
    parent="${post_id}">
  </v-postbox>`;
}

/**
 *
 * @param {number} post_id
 */
function toggleReplies(post_id) {
  const commentsDiv = document.querySelectorAll(`.comments-for-${post_id}`);
  commentsDiv.forEach((div) => {
    const htmlDiv = /** @type {HTMLElement} */ (div);
    if (htmlDiv.style.display === "none" || htmlDiv.style.display === "") {
      htmlDiv.style.display = "block";
    } else {
      htmlDiv.style.display = "none";
    }
  });
}
