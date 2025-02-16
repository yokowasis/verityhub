class Profile extends HTMLElement {
  constructor() {
    super();
  }

  static get observedAttributes() {
    return ["handler"];
  }

  attributeChangedCallback(name) {
    if (name === "handler") {
      this.render();
    }
  }

  connectedCallback() {
    this.render();
  }

  render() {
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

class Logo extends HTMLElement {
  connectedCallback() {
    this.render();
  }

  render() {
    this.innerHTML = /*html*/ `
      <h1 style="font-size: 2rem;" class="text-center">
        <a href="/" style="text-decoration:none;color:#fff"><img style="height: 50px;" src="/assets/images/logo-removebg-preview.png" />
        Verity<span style="color: #03a9f4;">Hub</span></a>
      </h1>    
    `;
  }
}

customElements.define("v-logo", Logo);

class Postbox extends HTMLElement {
  connectedCallback() {
    this.render();
  }

  render() {
    const id = this.getAttribute("id");
    const parent = this.getAttribute("parent") || "";
    const type = this.getAttribute("type") || "post";

    const w =
      /** @type {import("../../types").WInput} */
      (/** @type {*} */ (window));

    if (type !== "post" && type !== "article" && type !== "comment") return;

    this.innerHTML = /*html*/ `
      <cs-rtf
        toolbar="bold italic underline image"
        id="${id}-newpost"
        rows="2"
        placeholder="What's on your mind?"
        server="/"
      ></cs-rtf>
      <button type="button" class="btn btn-block btn-secondary" id="${id}-btn">
        <i class="fas fa-paper-plane"></i> Publish
      </button>
      <button type="button" class="btn btn-block btn-primary" id="${id}-newarticle-btn">
        <i class="fas fa-newspaper"></i> New Article
      </button>
    `;

    const newArticleBtn = document.getElementById(`${id}-newarticle-btn`);
    if (newArticleBtn) {
      newArticleBtn.addEventListener("click", () => {
        w.location.href = "/new-article";
      });
    }

    const postBtn = document.getElementById(`${id}-btn`);
    if (postBtn) {
      postBtn.addEventListener("click", async () => {
        const content = w.getVal(`${id}-newpost`);
        w.toast.loading("Please Wait ...");
        const r = await w.post(content, type, parent);
        if (r.message === "Post Success !") {
          w.toast.success("Post Success !");
          if (type === "comment") {
            const postid = document.getElementById(id || "");
            if (!postid) return;

            const postElement = postid.closest(".post");
            if (!postElement) return;

            const commentElement = document.createElement("div");
            commentElement.className = `comment ml-5 comments-for-${parent} d-block`;
            commentElement.id = `comment-${id}`;

            commentElement.innerHTML = /*html*/ `
              <v-profile
                fullname="${r.data.full_name}" 
                handler="${r.data.username}"
                avatar="${r.data.avatar}"
              ></v-profile>
              <div class="content">
                ${content}
              </div>
              <hr/>
            `;

            postElement.insertAdjacentElement("afterend", commentElement);

            const replyBoxDiv = document.getElementById(`reply-box-${parent}`);
            if (replyBoxDiv) {
              replyBoxDiv.innerHTML = "";
            }

            return;
          }

          w.location.reload();
        } else {
          w.toast.error(r.message);
        }
      });
    }
  }
}

customElements.define("v-postbox", Postbox);
