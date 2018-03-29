// Replace all links with target _blank to maintain persistence
var links = document.links;
for (var i = 0; i < links.length; i++) {
     links[i].target = "_blank";
}
'Done'
