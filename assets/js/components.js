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
