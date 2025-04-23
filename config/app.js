// noinspection JSJQueryEfficiency,JSUnresolvedReference,DuplicatedCode

function getKCHost() {
    let baseURL = window.location.protocol + "//" + window.location.host;
    setTimeout(function () {
        baseURL = baseURL + '/sp-auth'
        kcAuth(baseURL);
    }, 2000)
}

function kcAuth(kcBaseURL) {
    const authURL = `${kcBaseURL}/sp-auth`;
    const keycloak = new Keycloak({
        "auth-server-url": authURL,
        url: kcBaseURL,
        realm: 'my-sp',
        clientId: 'my-sp-client',
        "enable-cors": true,
        "public-client": false,
    });
    keycloak.init({
        onLoad: 'login-required',
        checkLoginIframe: false,
        promiseType: 'native',
        flow: 'implicit'
    }).then(authenticated => {
        console.log("Authenticated.");
        console.log(keycloak);
        window.keycloak = keycloak;
        const payload = parseJWT(keycloak.token);
        $('#token').html(JSON.stringify(payload, null, 2)); // The '2' specifies a 2-space indentation
        $('.editor').show();
        $('.loader').hide();
        // this.setState({keycloak: keycloak, authenticated: authenticated});
    }).catch(error => {
        console.error("Keycloak initialization error:", error);
    });
}

$(document).ready(function () {
    $("#idp-btn").on("click", function () {
        window.location.href = 'http://localhost/idp'
    });
});

$(document).ready(function () {
    $("#btn-logout").on("click", function () {
        window.location.href = "http://localhost/sp-auth/realms/my-sp/protocol/openid-connect/logout";
    });
});

function parseJWT(token) {
    if (!token) {
        throw new Error("Token is required");
    }
    const parts = token.split('.');
    if (parts.length !== 3) {
        throw new Error("Invalid JWT format");
    }
    const payload = parts[1];
    // Decode the payload from Base64Url
    const decodedPayload = JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')));
    return decodedPayload;
}