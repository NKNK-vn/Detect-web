import './prototype';
// BEGIN OF DECLARE VARIABLE
type webStates = 'safe' | 'unsafe' | 'critical' | 'processing';
interface ICachedWebsite {
    state?: webStates;
    off?: boolean;
    sample?: string;
}

// Init value
const LOCAL_CACHED_KEY = 'ExCached';
const LOCAL_WEB_HIDE_KEY = 'ExHide';
let webCaches: { [key: string]: ICachedWebsite } = JSON.parse(localStorage.getItem(LOCAL_CACHED_KEY) || '{}');
let hideImages = JSON.parse(localStorage.getItem(LOCAL_WEB_HIDE_KEY) || 'true');
let currentTab: chrome.tabs.Tab;
let loading = false;
// BEGIN OF EVENT HANDLE
/**
 * Process all processing state
 */
setInterval(async () => {
    if (loading) {
        return;
    }
    loading = true;
    for (let key of Object.keys(webCaches)) {
        if (webCaches[key]?.state === 'processing') {
            webCaches[key].state = (await callApiVerifyURL(webCaches[key].sample)) || 'processing';
            console.log('<i> Recall server for:', key, ' - Result:', webCaches[key].state);
            if (currentTab.url.domain() === webCaches[key].sample.domain()) {
                changeIconBaseOnState(webCaches[key].state || 'processing');
                updateWebImages();
            }
        }
    }
    loading = false;
    localStorage.setItem(LOCAL_CACHED_KEY, JSON.stringify(webCaches));
    localStorage.setItem(LOCAL_WEB_HIDE_KEY, JSON.stringify(hideImages));
}, 1000);
/**
 * On change tab
 */
chrome.tabs.onActivated.addListener((tabInfo) => {
    chrome.tabs.get(tabInfo.tabId, (tab) => {
        if (!currentTab || currentTab.id !== tab.id) {
            console.log('<i> Call onActive:', tab.url);
            currentTab = tab;
            // TODO: Update web
            changeIconBaseOnState(webCaches[currentTab.url.domain()]?.state || 'processing');
        }
    });
});

/**
 * On tabs update
 */
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
    if (tabId === currentTab.id && changeInfo?.status === 'complete') {
        console.log('<i> Call onUpdate:', tab.url);
        console.log('<i> Call onUpdate infos:', changeInfo);
        currentTab = tab;
        const domain = tab.url.domain();
        if (!webCaches[domain]?.state) {
            updateWebImages();
            console.log('<i> Detect new domain:', domain);
            changeIconBaseOnState('processing');
            webCaches[domain] = { sample: tab.url, off: false };
            webCaches[domain].state = (await callApiVerifyURL(tab.url)) || 'processing';
            console.log('<i> Server response value:', webCaches[domain].state);
        }
        changeIconBaseOnState(webCaches[domain]?.state || 'processing');
        updateWebImages();
        // TODO: update all image
    }
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
                if (!webCaches[currentTab.url.domain()]) {
                    response({ state: 'processing', off: false });
                } else {
                    response(webCaches[currentTab.url.domain()]);
                }
                break;
            case 'get_hide_value':
                response(hideImages);
                break;
            case 'disabled_page':
                if (typeof message.data === 'boolean') {
                    // TODO Update all image
                    if (webCaches[currentTab.url.domain()]) {
                        webCaches[currentTab.url.domain()].off = message.data;
                    }
                    response(true);
                } else {
                    response(false);
                }
                break;
            case 'set_hide_value':
                if (typeof message.data === 'boolean') {
                    hideImages = message.data;
                    // TODO Update all image
                    updateWebImages();
                    response(true);
                } else {
                    response(false);
                }
                break;
            default:
                response(false);
                break;
        }
    }
});

// BEGIN OF FUNCTIONS
/**
 * Change icon of extension base on web safe state
 * @param state State of icon that need to be changed
 */
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

/**
 * Verify URL of website
 * @param {string} url URL of website that need to be verified
 * @param {function} cb Callback after done, will response from -1 to 1
 */
function callApiVerifyURL(url = ''): Promise<webStates | false> {
    // Fake calling
    const fakeTimes = [100, 300, 599, 2139, 3000];
    return new Promise((rs, rj) => {
        if (typeof url !== 'string' || url.length < 3) {
            rs(false);
            return;
        }
        setTimeout(() => {
            let items: webStates[] = ['safe', 'unsafe', 'critical', 'processing'];
            rs(items[Math.floor(Math.random() * items.length)]);
            return;
        }, fakeTimes[Math.floor(Math.random() * fakeTimes.length)]);
    });
}

/**
 * Hide all images on unsafe website if hide is enabled
 */
function updateWebImages() {
    if (hideImages && webCaches[currentTab.url.domain()]?.state !== 'safe') {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            chrome.tabs.connect(tabs[0].id).postMessage('hideImages');
        });
    } else {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            chrome.tabs.connect(tabs[0].id).postMessage('showImages');
        });
    }
}
