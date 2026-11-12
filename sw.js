/* ==========================================================================
   JagX Pulse — service worker
   Offline reading: caches the shell + every story image so a reader can
   open the edition with no connection. Bump CACHE_VERSION on each edition.
   ========================================================================== */

const CACHE_VERSION = "jagx-pulse-v1";
const SHELL_CACHE = CACHE_VERSION + "-shell";
const IMAGE_CACHE = CACHE_VERSION + "-images";

/* The app shell — everything needed to render the edition offline. */
const SHELL_ASSETS = [
  "./",
  "./index.html",
  "./styles.css",
  "./manifest.json",
  "./data/stories.json",
  "./icons/crest.svg",
  "./icons/icon-maskable.svg"
];

/* Every story image in this edition — served through the /images/* rewrite. */
const STORY_IMAGES = [
  "./images/world-nkorea.webp",
  "./images/africa-drc.webp",
  "./images/africa-sa.webp",
  "./images/nigeria-borrowing.webp",
  "./images/nigeria-inec.webp",
  "./images/business-dangote.webp",
  "./images/business-markets.webp",
  "./images/tech-meta.webp",
  "./images/sports-flamingos.webp",
  "./images/ent-latingrammy.webp",
  "./images/health-ebola.webp",
  "./images/health-lenacapavir.webp",
  "./images/science-cop31.webp"
];

/* Story images are bundled in /images/ in the repository. When a photo is not
   bundled, vercel.json rewrites that path to the original source URL, so the
   service worker follows the redirect and caches whatever the host returns. */

/* ---------- install: pre-cache the shell and the images ---------- */
self.addEventListener("install", event => {
  event.waitUntil(
    (async () => {
      const shell = await caches.open(SHELL_CACHE);
      // addAll fails the whole install if one file 404s — add individually instead
      await Promise.all(
        SHELL_ASSETS.map(url =>
          shell.add(new Request(url, { cache: "reload" })).catch(() => null)
        )
      );
      const imgs = await caches.open(IMAGE_CACHE);
      await Promise.all(
        STORY_IMAGES.map(url =>
          imgs.add(new Request(url, { cache: "reload" })).catch(() => null)
        )
      );
      await self.skipWaiting();
    })()
  );
});

/* ---------- activate: drop caches from older editions ---------- */
self.addEventListener("activate", event => {
  event.waitUntil(
    (async () => {
      const keys = await caches.keys();
      await Promise.all(
        keys
          .filter(k => k.startsWith("jagx-pulse-") && !k.startsWith(CACHE_VERSION))
          .map(k => caches.delete(k))
      );
      if (self.registration.navigationPreload) {
        await self.registration.navigationPreload.disable();
      }
      await self.clients.claim();
    })()
  );
});

/* ---------- fetch strategy ---------- */
self.addEventListener("fetch", event => {
  const req = event.request;

  // Only handle GETs on our own origin.
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // Navigations: network first, fall back to the cached shell (offline reading).
  if (req.mode === "navigate") {
    event.respondWith(
      (async () => {
        try {
          const fresh = await fetch(req);
          const cache = await caches.open(SHELL_CACHE);
          cache.put("./index.html", fresh.clone());
          return fresh;
        } catch (e) {
          const cache = await caches.open(SHELL_CACHE);
          return (
            (await cache.match("./index.html")) ||
            (await cache.match("./")) ||
            new Response(
              "<h1>JagX Pulse is offline</h1><p>Reconnect to load the latest edition.</p>",
              { headers: { "Content-Type": "text/html; charset=utf-8" }, status: 200 }
            )
          );
        }
      })()
    );
    return;
  }

  // Images: cache first — they never change within an edition.
  if (req.destination === "image") {
    event.respondWith(
      (async () => {
        const cache = await caches.open(IMAGE_CACHE);
        const hit = await cache.match(req);
        if (hit) return hit;
        try {
          const fresh = await fetch(req);
          if (fresh && fresh.status === 200) cache.put(req, fresh.clone());
          return fresh;
        } catch (e) {
          return new Response("", { status: 504, statusText: "Offline" });
        }
      })()
    );
    return;
  }

  // Everything else (css, js, json, fonts): stale-while-revalidate.
  event.respondWith(
    (async () => {
      const cache = await caches.open(SHELL_CACHE);
      const hit = await cache.match(req);
      const network = fetch(req)
        .then(res => {
          if (res && res.status === 200 && res.type === "basic") {
            cache.put(req, res.clone());
          }
          return res;
        })
        .catch(() => null);
      return hit || (await network) || new Response("", { status: 504, statusText: "Offline" });
    })()
  );
});

/* ---------- allow the page to trigger an update ---------- */
self.addEventListener("message", event => {
  if (event.data === "SKIP_WAITING") self.skipWaiting();
});
