/* Native app bridge helpers. */
(function () {
  "use strict";

  const output = document.getElementById("output");
  const echoOutput = document.getElementById("echoOutput");

  function send(action, payload) {
    const msg = JSON.stringify({ action: action, payload: payload || {} });
    if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.nativeApp) {
      window.webkit.messageHandlers.nativeApp.postMessage(msg);
    } else {
      console.warn("native bridge unavailable:", msg);
    }
  }

  window.nativeAppReceive = function (reply) {
    if (output) output.textContent = JSON.stringify(reply, null, 2);
  };

  const pingBtn = document.getElementById("pingBtn");
  if (pingBtn) pingBtn.addEventListener("click", () => send("ping", {}));

  const echoBtn = document.getElementById("echoBtn");
  if (echoBtn) echoBtn.addEventListener("click", () => {
    const value = document.getElementById("echoInput").value;
    send("echo", { text: value });
    if (echoOutput) echoOutput.textContent = "Sent: " + value;
  });
})();