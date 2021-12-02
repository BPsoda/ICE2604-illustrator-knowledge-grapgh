 var svg = document.getElementById("svg");
    var svgPanel = document.getElementById("svgPanel");
    var gridSvg = document.getElementById("grid");
    var width = 1500;  //设置svg整体的宽和高
    var height = 900;
    var gridLength = 20; //定义网格的大小
    var scale=1;

    svg.setAttribute("width",width);
    svg.setAttribute("height",height);
    /**
     * js创建svg元素
     * @param {String} tag svg的标签名
     * @param {Object} svg元素的属性
     */
    function resetSVG(tag, attrs) {
        var element = document.createElementNS('http://www.w3.org/2000/svg', tag);
        for (var k in attrs) {
            element.setAttribute(k, attrs[k]);
        }
        return element;
    }

    /**
 * svg放缩
 * {Float} num 放缩的倍数
 */
function zoom(num){
    scale *= num;
    svgPanel.setAttribute("transform","scale("+scale+")");
    drawGrid(gridSvg,width*(1/scale),height*(1/scale),gridLength);
}

////绑定鼠标滑轮事件
//if(document.addEventListener){
//    document.addEventListener('DOMMouseScroll',scrollZoom,false);
//}
//window.onmousewheel=document.onmousewheel=scrollZoom;
//
///**
// * 滑轮滚动处理事件，向上滚放大
// * {Object} e 事件对象
// */
//function scrollZoom(e){
//    e=e || window.event;
//    //e.detail用来兼容 FireFox
//    e.wheelDelta>0 || e.detail >0?zoom(1.1):zoom(0.9);
//}