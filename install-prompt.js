/**
 * Install Prompt — erateapp.com PWA
 * Captures the beforeinstallprompt event and shows a custom install banner.
 * Platform-aware: shows native prompt on Chrome/Edge, manual instructions on iOS/Firefox.
 */
(function () {
  'use strict';

  const DISMISS_KEY = 'erateapp_install_dismissed';
  const DISMISS_DAYS = 7;

  // Check if already dismissed
  function isDismissed() {
    try {
      const ts = localStorage.getItem(DISMISS_KEY);
      if (!ts) return false;
      return Date.now() - parseInt(ts, 10) < DISMISS_DAYS * 86400000;
    } catch (e) { return false; }
  }

  function dismiss() {
    try { localStorage.setItem(DISMISS_KEY, Date.now().toString()); } catch (e) {}
    hideBanner();
  }

  // Detect platform
  function getPlatform() {
    var ua = navigator.userAgent || '';
    if (/iPad|iPhone|iPod/.test(ua) && !window.MSStream) return 'ios';
    if (/android/i.test(ua)) return 'android';
    return 'desktop';
  }

  function isStandalone() {
    return window.matchMedia('(display-mode: standalone)').matches ||
           window.navigator.standalone === true;
  }

  var deferredPrompt = null;
  var banner = null;

  function createBanner(platform) {
    if (banner) return;
    banner = document.createElement('div');
    banner.id = 'pwa-install-banner';
    banner.setAttribute('role', 'alert');

    var message, buttonText, instructions = '';
    if (platform === 'ios') {
      message = 'Install E-Rate App on your device';
      buttonText = 'How to Install';
      instructions = '<p style="margin:8px 0 0;font-size:13px;color:#64748b;">Tap the <strong>Share</strong> button <span style="font-size:16px;">⎙</span> then <strong>"Add to Home Screen"</strong></p>';
    } else if (deferredPrompt) {
      message = 'Install E-Rate App for quick access';
      buttonText = 'Install App';
    } else {
      message = 'Install E-Rate App on your device';
      buttonText = 'How to Install';
      instructions = '<p style="margin:8px 0 0;font-size:13px;color:#64748b;">Open your browser menu and select <strong>"Install App"</strong> or <strong>"Add to Home Screen"</strong></p>';
    }

    banner.innerHTML =
      '<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">' +
        '<div style="display:flex;align-items:center;gap:12px;flex:1;min-width:200px;">' +
          '<img src="/logo.PNG" alt="E-Rate App" style="width:44px;height:44px;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,.12);">' +
          '<div>' +
            '<strong style="font-size:15px;color:#1e293b;">' + message + '</strong>' +
            instructions +
          '</div>' +
        '</div>' +
        '<div style="display:flex;gap:8px;align-items:center;">' +
          '<button id="pwa-install-btn" style="padding:10px 24px;background:linear-gradient(135deg,#1976d2,#0d47a1);color:#fff;border:none;border-radius:8px;font-weight:600;font-size:14px;cursor:pointer;white-space:nowrap;transition:transform .15s;">' + buttonText + '</button>' +
          '<button id="pwa-dismiss-btn" style="padding:8px;background:none;border:none;cursor:pointer;color:#94a3b8;font-size:20px;line-height:1;" title="Dismiss">&times;</button>' +
        '</div>' +
      '</div>';

    banner.style.cssText = 'position:fixed;bottom:0;left:0;right:0;z-index:9999;background:#fff;border-top:1px solid #e2e8f0;box-shadow:0 -4px 20px rgba(0,0,0,.1);padding:16px 24px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;transform:translateY(100%);transition:transform .35s ease;';

    document.body.appendChild(banner);

    // Animate in
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        banner.style.transform = 'translateY(0)';
      });
    });

    document.getElementById('pwa-dismiss-btn').addEventListener('click', dismiss);
    document.getElementById('pwa-install-btn').addEventListener('click', function () {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then(function (result) {
          if (result.outcome === 'accepted') hideBanner();
          deferredPrompt = null;
        });
      }
      // iOS / fallback — button already shows instructions, just keep it visible
    });
  }

  function hideBanner() {
    if (banner) {
      banner.style.transform = 'translateY(100%)';
      setTimeout(function () { if (banner && banner.parentNode) banner.parentNode.removeChild(banner); banner = null; }, 400);
    }
  }

  // Listen for the native install prompt
  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferredPrompt = e;
    if (!isDismissed() && !isStandalone()) {
      createBanner(getPlatform());
    }
  });

  // Show banner for iOS (no beforeinstallprompt event)
  if (getPlatform() === 'ios' && !isStandalone() && !isDismissed()) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () { createBanner('ios'); });
    } else {
      createBanner('ios');
    }
  }

  // If already installed, never show
  window.addEventListener('appinstalled', function () { hideBanner(); });
})();
