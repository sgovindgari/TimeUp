$( document ).ready(function() {
    
    $("#addTask").click(function() {
        var description = $("#description").val();
        var duration = $("#duration").val();

        $.post("/tasks/new", {"description": description, "duration": duration}, 
            function(data) { 
                getTasks();
            });
    }); 
       
});

function getTasks() {
    $.get("/tasks", 
            function(data) {
                if (data.status == "success") {
                    alert("backend login ok");
                } else {
                    alert("backend login failed");
                }
            });
    
}
