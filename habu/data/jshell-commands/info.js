// Get browser info
data = {}
data['user-agent'] = window.navigator.userAgent;
data['location'] = window.location.href;
data['java-enabled'] = window.navigator.javaEnabled();
data['platform'] = window.navigator.platform;
data['app-code-name'] = window.navigator.appCodeName;
data['app-name'] = window.navigator.appName;
data['app-version'] = window.navigator.appVersion;
data['cookie-enabled'] = window.navigator.cookieEnabled;
data['language'] = window.navigator.language;
data['online'] = window.navigator.onLine;
JSON.stringify(data);

