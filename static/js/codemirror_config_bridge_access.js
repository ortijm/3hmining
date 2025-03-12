(function( $ ) {
$(document).ready(function() {
    var idQueryELement = document.getElementById('id_request');
    var editor = new CodeMirror.fromTextArea(idQueryELement, {
        width: "90%",
        height: "600px",
        stylesheet: ["/static/css/codemirror/codemirror.css"],
        content: document.getElementById("id_request").value,
        mode: 'application/json',
        json: true,
        lineWrapping: true
    });
    var totalLines = editor.lineCount();
    editor.autoFormatRange({line:0, ch:0}, {line:totalLines});

});
}( django.jQuery ));
