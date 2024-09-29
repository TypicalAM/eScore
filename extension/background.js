chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('received message: ', message);
    if (message.action === 'setBadge') {
        chrome.action.setBadgeText({ text: message.text });
        chrome.action.setBadgeBackgroundColor({ color: message.color }); 
    }

    if (message.action === 'updateStatus') {
        console.log('updating status to: ', message.text);
        chrome.action.openPopup();
	chrome.runtime.sendMessage(message);
    }
});
