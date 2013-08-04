$( document ).ready(function() {
    
    getTasks();
    $("#addTask").click(function() {
        var description = $("#description").val();
        var duration = $("#duration").val();

        $.post("/tasks/new", {"description": description, "duration": duration}, 
            function(data) { 
                getTasks();
            });
    });

    $("#getTask").click(function() {

        window.location = "/gettask";

    }); 
       
});

function getTasks() {
    // data :{[{description, duration},]}
    $.get("/tasks", 
            function(data) {
                $("#tasks").text("");

                for (var i = 0; i < data.task_list.length; i++) {
                    //var tempelem = document.createElement('di
                    var description = data.task_list[i].description;
                    var duration = data.task_list[i].duration;
                    $("#tasks").append("<li class='row'>" + "<div class='description'>" + description + "</div> <div class='duration'>" + duration + " minutes </div> </li>");
                }
            });
}
