function getCurrentDate() {
    let x = new Date()
    return date2str(x, 'yyyy-MM-dd hh:mm:ss')
}

function date2str(x, y) {
    let z = { y: x.getFullYear(), M: x.getMonth() + 1, d: x.getDate(), h: x.getHours(), m: x.getMinutes(), s: x.getSeconds() };
    return y.replace(/(y+|M+|d+|h+|m+|s+)/g, function (v) { 
        return ((v.length > 1 ? "0" : "") + eval('z.' + v.slice(-1))).slice(-(v.length > 2 ? v.length : 2)) });
}

function tsToDateStr(ts){
    return date2str(new Date(ts), 'yyyy-MM-dd hh:mm:ss')
}

export {tsToDateStr}