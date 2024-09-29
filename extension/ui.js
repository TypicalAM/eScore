console.log('UI script loaded');

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'updateStatus') {
    document.getElementById('mainFactor').innerHTML = request.text;
  }
});
