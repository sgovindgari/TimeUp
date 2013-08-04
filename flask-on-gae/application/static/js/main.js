$( document ).ready(function() {
    
    getTasks();
    $("#addTask").click(function() {
        var description = $("#description").val();
        var duration = $("#duration").val();
        var isPrivate = $("#isPrivate").val();

        $.post("/tasks/new", 
            {"description": description, 
                "duration": duration,
               "isPrivate": isPrivate}, 
            function(data) { 
                getTasks();
            });
    });

    $("#givetask").click(function() {
        var duration = $("#duration2")
        $.get("/gettasks", {"duration": duration}, 
            function(data){
                displayTask(data);
            });

    });

    $("#getTask").click(function() {
        window.location = "/gettask";
    }); 

    $("#isPrivate").click(function() {
        console.log($(this).attr("value"));
        if ($(this).attr("value") == "true") {
            $(this).attr("value", "false");
            $(this).attr("class", "btn btn-danger");
        } else {
            $(this).attr("value", "true");
            $(this).attr("class", "btn btn-primary");
        }
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
                    var key = data.task_list[i].key;
                    var done = data.task_list[i].done;
                    var isPrivate = data.task_list[i].isPrivate;

                    $("#tasks").append("<li class='row' value='" + key + "'>" +
                            "<div class='done'>" + done + " </div>" + 
                            "<div class='isPrivate'>" + isPrivate + " </div>" + 
                            "<div class='description'>" + description + "</div>" + 
                            "<div class='duration'>" + duration + " minutes </div>" + 
                            "</li>");
                }
            });
}
