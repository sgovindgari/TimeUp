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
        var me = $("#me")
        var friend = $("#friend")

        $.get("/gettasks", {"duration": duration, "me": me, "friend": friend}, 
            function(data){
                $("#tasks").text("");
                for (var i = 0; i < data.task_list.length; i++) {
                    //var tempelem = document.createElement('di
                    var description = data.task_list[i].description;
                    var duration = data.task_list[i].duration;
                    var key = data.task_list[i].key;

                    $("#tasks").append("<li class='row' value='" + key + "'>" +
                            "<div class='description'>" + description + "</div>" + 
                            "<div class='duration'>" + duration + " minutes </div>" + 
                            "</li>");
                }
            });

    });

    $("#getTask").click(function() {
        window.location = "/gettask";
    }); 

    $("#isPrivate").click(function() {
        console.log($(this).attr("value"));
        if ($(this).attr("value") == "false") {
            $(this).attr("value", "true");
            $(this).attr("class", "btn btn-primary");
            $(this).text("private");
        } else {
            $(this).attr("value", "false");
            $(this).attr("class", "btn btn-inverse");
            $(this).text("public");
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
                    var timestamp = data.task_list[i].timestamp;

                    $("#tasks").append("<li class='row' value='" + key + "'>" +
                            "<div class='done'>" + done + " </div>" + 
                            "<div class='isPrivate'>" + isPrivate + " </div>" + 
                            "<div class='description'>" + description + "</div>" + 
                            "<div class='duration'>" + duration + " minutes </div>" + 
                            "<div class='timestamp'>" + timestamp + "</div>" + 
                            "</li>");
                }
            });
}
