webpackJsonp([5],{1248:function(e,t,n){"use strict";function o(){var e=document.getElementById("notebook-container")||document.getElementById("dashboard-container")||document.getElementsByClassName("main-container")[0]||document.getElementsByClassName("bk-root")[0],t=i(e)+30;t!=this.previousHeight&&(this.previousHeight=t,parent.postMessage({iFrameHeight:t},"*"))}function i(e){var t=e.offsetHeight,n=getComputedStyle(e);return t+=parseInt(n.marginTop)+parseInt(n.marginBottom)}Object.defineProperty(t,"__esModule",{value:!0}),t.postHeight=o},2819:function(e,t,n){n(2820),e.exports=n(2822)},2820:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var o=n(2821),i=n(1248);new(function(){function e(){document.addEventListener("DOMContentLoaded",this.domLoaded.bind(this)),window.addEventListener("load",this.pageLoaded.bind(this),!1),window.addEventListener("resize",i.postHeight,!1)}return e.prototype.domLoaded=function(){this.setKaggleAnchorsToLoadInPage(),this.setAnchorsToScrollIntoView(),this.startUpdatingHeight(),o.CellHiding.register()},e.prototype.pageLoaded=function(){this.stopUpdatingHeight()},e.prototype.setKaggleAnchorsToLoadInPage=function(){Array.prototype.slice.call(document.getElementsByTagName("a")).forEach(function(e){"www.kaggle.com"===e.hostname&&(e.target="_top")})},e.prototype.setAnchorsToScrollIntoView=function(){Array.prototype.slice.call(document.getElementsByTagName("a")).forEach(function(e){var t=e.hash;null!=t&&t.startsWith("#")&&e.hostname===document.location.hostname&&(e.target="_self",e.onclick=function(){return parent.postMessage({anchorClicked:!0},"*"),document.getElementById(t.substr(1)).scrollIntoView(),!1})})},e.prototype.startUpdatingHeight=function(){i.postHeight(),this.heightIntervalHandle=setInterval(i.postHeight,200)},e.prototype.stopUpdatingHeight=function(){clearTimeout(this.heightIntervalHandle),i.postHeight()},e}())},2821:function(e,t,n){"use strict";(function(e){Object.defineProperty(t,"__esModule",{value:!0});var o=n(1),i=n(48),s=n(1248),a=function(){function t(){}return t.register=function(){var e=document.getElementsByClassName("_kg_hide-input-true"),n=document.getElementsByClassName("_kg_hide-output-true");t.addControls(e,"Code"),t.addControls(n,"Output")},t.addControls=function(t,n){Array.prototype.slice.call(t).forEach(function(t){var o=document.createElement("div");t.insertBefore(o,t.firstChild),i.render(e.createElement(r,{type:n,cell:t}),o)})},t}();t.CellHiding=a;var r=function(t){function n(e){var n=t.call(this,e)||this;return n.onClick=function(){var e=n.props.cell,t=!n.state.visible;t?e.classList.add(n.showAreaClassName):e.classList.remove(n.showAreaClassName),n.setState({visible:t}),s.postHeight()},n.showAreaClassName="cell-area-visible--"+n.props.type,n.state={visible:!1},n}return o.__extends(n,t),n.prototype.render=function(){return e.createElement("div",{className:"cell-visibility-toggle",onClick:this.onClick},this.state.visible?"Hide":this.props.type)},n}(e.Component)}).call(t,n(0))},2822:function(e,t){}},[2819]);