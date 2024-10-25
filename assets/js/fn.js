async function isAuth() {
  /** @type {import("../../types").DBClient} */
  const db = /** @type {*} */ (window).db;

  const user = await db?.auth?.getUser();

  if (user?.data?.user) {
    return true;
  } else {
    return false;
  }
}

async function getUser() {
  /** @type {import("../../types").DBClient} */
  const db = /** @type {*} */ (window).db;

  const user = (await db.auth.getUser()).data.user;
  return user;
}

async function getUserBio() {
  /** @type {import("../../types").DBClient} */
  const db = /** @type {*} */ (window).db;

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

async function initLeftSidebar() {
  /** @type {import("../../types").DBClient} */
  const db = /** @type {*} */ (window).db;

  /** @type {import("../../types").WInput} */
  const w = /** @type {*} */ (window);

  if (await isAuth()) {
    const user = await getUser();
    const bio = await getUserBio();
    if (!user) return;

    const userprofile = document.getElementById("userprofile");

    if (!userprofile) {
      return;
    }

    userprofile.setAttribute("fullname", bio?.full_name || "");
    userprofile.setAttribute("avatar", bio?.avatar || "");
    userprofile.setAttribute("handler", bio?.handler || "");

    const newPostWrapper = document.getElementById("newpostwrapper");
    if (!newPostWrapper) return;

    newPostWrapper.innerHTML = /*html*/ `        
        <c-input toolbar="bold italic underline image" type="rtf" id="newpost" rows="2"
          placeholder="What's on your mind?"></c-input>
        <button type="button" class="btn btn-block btn-primary" id="post"><i class="fas fa-paper-plane"></i>
          Publish</button>          
          `;

    const postBtn = document.getElementById("post");

    if (!postBtn) {
      return;
    }

    postBtn.addEventListener("click", async () => {
      w.toast.loading("Please Wait ...");

      const content = w.getVal("newpost");

      if (!content) {
        return;
      }

      if (!user) {
        return;
      }

      const summary = await getSummary(content);
      const vector = await getVector(summary);
      const bio = await getUserBio();

      const { data, error } = await db.from("posts").insert({
        content,
        user_id: user.id,
        user: bio?.id,
        summary,
        content_vec: JSON.stringify(vector),
      });

      if (error) {
        w.toast.error(error.message);
      }

      w.toast.success("Post Success !");

      w.setVal("newpost", "");
    });
  } else {
    const newPostWrapper = document.getElementById("newpostwrapper");
    if (!newPostWrapper) return;

    newPostWrapper.innerHTML = /*html*/ `
    <div class="text-center">
      <img src="/assets/images/mascott-removebg-preview.png" style="width: 200px;" />
      <p><b>Welcome to VerityHub!</b></p>

      <p>At VerityHub, we believe in creating meaningful, trustworthy connections where your privacy comes first. This is more than just social media; it's a place for genuine discovery, insights, and engagement, backed by powerful, privacy-focused technology.</p>
    </div>
`;
  }
}

async function fetchPosts() {
  /** @type {import("../../types").DBClient} */
  const db = /** @type {*} */ (window).db;

  const { data, error } = await db
    .from("posts")
    .select(
      `
      id,
      content,
      user (
        full_name,
        handler,
        avatar
      )
      `
    )
    .limit(10)
    .order("created_at", { ascending: false });

  if (error) {
    return;
    console.log(error);
  }

  const posts = data;

  if (!posts) {
    return;
  }

  const postWrapper = document.getElementById("pills-posts");

  if (!postWrapper) {
    return;
  }

  postWrapper.innerHTML = /*html*/ `
    ${posts.map((post) => {
      return /*html*/ `
        <div class="post">
          <v-profile fullname="${post.user.full_name}" handler="${post.user.handler}" avatar="${post.user.avatar}"></v-profile>
          <div class="content">
            ${post.content}
          </div>
        </div>
      `;
    })}
  `;
}
