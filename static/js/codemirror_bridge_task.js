(function( $ ) {
$(document).ready(function() {
    var idQueryELement = document.getElementById('id_query'); 
    var editor = new CodeMirror.fromTextArea(idQueryELement, {
        width: "90%",
        height: "600px",
        stylesheet: ["/static/css/codemirror/codemirror.css"],
        content: document.getElementById("id_query").value,
        mode: 'text/x-sql'
    });

});
}( django.jQuery ));
