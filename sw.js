/* LifeBridge Lens service worker: offline pages + offline fallback page.
 * Registered on every page by i18n.js. Version the CACHE name to update.
 * Every CORE entry must exist, or the whole install fails.
 */
const CACHE = "lens-v11";
const CORE = [
    "/",
    "offline.html",
    "index.html",
    "explain.html",
    "tracker.html",
    "dates.html",
    "style.css",
    "i18n.js",
    "chatbot.js",
    "site.webmanifest",
    "icons/document.svg",
    "icons/icon-192.png",
    "icons/icon-512.png"
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE)
            .then((cache) => cache.addAll(CORE))
            .then(() => self.skipWaiting())
    );
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys()
            .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
            .then(() => self.clients.claim())
    );
});

function isHtmlRequest(req) {
    if (req.mode === "navigate") return true;
    const type = req.headers.get("accept") || "";
    return type.indexOf("text/html") !== -1;
}

self.addEventListener("fetch", (event) => {
    const req = event.request;
    if (req.method !== "GET") return;
    const url = new URL(req.url);
    if (url.origin !== self.location.origin) return;
    if (url.pathname === "/explain" || url.pathname === "/ask" || url.pathname === "/sw.js" || url.pathname === "/lb-config.js") return;
    if (isHtmlRequest(req)) {
        // Pages: network first, so updates show right away.
        event.respondWith(
            fetch(req).then((res) => {
                if (res && res.ok) {
                    const copy = res.clone();
                    caches.open(CACHE).then((cache) => cache.put(req, copy));
                }
                return res;
            }).catch(() => {
                return caches.match(req).then((cached) => {
                    return cached || caches.match(req, { ignoreSearch: true });
                }).then((cached) => {
                    return cached || caches.match("offline.html");
                });
            })
        );
        return;
    }
    // Images, CSS and JS: cache first for speed and offline use.
    event.respondWith(
        caches.match(req).then((cached) => {
            if (cached) return cached;
            return fetch(req).then((res) => {
                if (res && res.ok) {
                    const copy = res.clone();
                    caches.open(CACHE).then((cache) => cache.put(req, copy));
                }
                return res;
            }).catch(() => {
                if (req.mode === "navigate") return caches.match("offline.html");
                throw new Error("offline");
            });
        })
    );
});
