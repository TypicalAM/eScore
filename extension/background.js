chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('received message: ', message);
    if (message.action === 'setBadge') {
        chrome.action.setBadgeText({ text: message.text });
        chrome.action.setBadgeBackgroundColor({ color: message.color }); 
    }
});
