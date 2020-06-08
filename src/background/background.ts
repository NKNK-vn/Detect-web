import './prototype';
// BEGIN OF DECLARE VARIABLE
type webStates = 'safe' | 'unsafe' | 'critical' | 'processing';
interface ICachedWebsite {
    state: webStates;
    off: boolean;
}

// Init value
let webCaches: { [key: string]: ICachedWebsite } = {};
let hideImages = false;
let currentTab: chrome.tabs.Tab;

// BEGIN OF EVENT HANDLE
/**
 * On change tab
 */
chrome.tabs.onActivated.addListener((tabInfo) => {
    chrome.tabs.get(tabInfo.tabId, (tab) => {
        if (!currentTab || currentTab !== tab) {
            currentTab = tab;
            // TODO: Update web
        }
    });
});

/**
 * On tabs update
 */
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (!currentTab || currentTab !== tab || currentTab.url !== tab.url) {
        currentTab = tab;
        // TODO: Update safe value for this web
    }
    // TODO: update all image
});

/**
 * On receive message from popup or contentJS
 */
chrome.runtime.onMessage.addListener((message: { from: string; action: string; data?: any }, sender, response) => {
    if (['content', 'popup'].indexOf(message.from) !== -1) {
        // Incoming message to handle
        console.log('<i> Incoming message from:', message.from);
        switch (message.action) {
            case 'get_safe_value':
                // TODO implement get safe value
                response('safe');
                break;
            case 'get_hide_value':
                response(hideImages);
                break;
            case 'set_hide_value':
                if (typeof message.data === 'boolean') {
                    hideImages = message.data;
                    // TODO Update all image
                    response(true);
                }
                response(false);
                break;
            default:
                response(false);
                break;
        }
    }
});

// BEGIN OF FUNCTIONS
function changeIconBaseOnState(state: webStates | 'default') {
    switch (state) {
        case 'processing': {
            chrome.browserAction.setIcon({ path: './images/Load.svg' }, () => true);
            break;
        }
        case 'safe': {
            chrome.browserAction.setIcon({ path: './images/Safe.svg' }, () => true);
            break;
        }
        case 'critical': {
            chrome.browserAction.setIcon({ path: './images/Warn.svg' }, () => true);
            break;
        }
        case 'unsafe': {
            chrome.browserAction.setIcon({ path: './images/Warn.svg' }, () => true);
            break;
        }
        // Handle other message
        default:
            chrome.browserAction.setIcon({ path: './images/128x128.png' }, () => true);
            break;
    }
}
