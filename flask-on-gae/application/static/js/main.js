$( document ).ready(function() {

    
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

    $("#giveTask").click(function() {
        var duration = $("#duration2").val();
        var me = $("#me").is(':checked');
        var friend = $("#friend").is(':checked');

        $.post("/givetask", {"duration": duration, "me": me, "friend": friend}, 
          function(data){
          $("#tasks").text("");
          for (var i = 0; i < data.task_list.length; i++) {
          //var tempelem = document.createElement('di
            var description = data.task_list[i].description;
            var duration = data.task_list[i].duration;
            var key = data.task_list[i].key;
            console.log(data.task_list[i].ownername)
            var username = data.task_list[i].ownername;


            $("#tasks").append("<li class='row' value='" + key + "'>" +
                "<div class='description'>" + description + "</div>" + 
                "<div class='duration'>" + duration + " minutes </div>" +
                "<div class='username'>" + username + "</div>" + 
                "</li>");
          }
          });

          });

        $("#getTask").click(function() {
            window.location = "/gettask";
            }); 

        $("#logout").click(function() {
            FB.logout(function(response) {
              $.get("/logout", function(data) {
                window.location = "/";
                });
              });
            });


      $("#isPrivate").click(function() {
          console.log($(this).attr("value"));
          if ($(this).attr("value") == 'true') {
          $(this).attr("value", "false");
          $(this).attr("class", "btn btn-inverse");
          $(this).text("public");
          } else {
          $(this).attr("value", "true");
          $(this).attr("class", "btn btn-primary");
          $(this).text("private");
          }
      });
});

window.onDeleteClicked = function(evt) {
    debugger; 
    var key = evt.currentTarget.getAttribute('data-key');
    console.log("deleting: " + key);
    deleteTask(key);
}      

window.onFinishClicked = function(evt) {
    var key = evt.currentTarget.getAttribute('value');
    var obj = evt.currentTarget;
    obj.style.opacity = 0.35;
    console.log("finishing: " + key);
    finishtask(key);
}      

function deleteTask(value){
    $.post("/deletetask", {"key": value}, function(data){
        console.log("deleting call out: " + value);
        getTasks();
    });
}
function finishtask(value) {
    $.post("/finishtask", {"key": value}, function(data) { 
        console.log("finishing call out: " + value);
        getTasks(); 
    });
}

function getTasks2() {
    // data :{[{description, duration},]}
    $.get("/tasksall", 
            function(data) {
                $("#tasks").text("");

                for (var i = 0; i < data.task_list.length; i++) {
                    //var tempelem = document.createElement('di
                    var description = data.task_list[i].description;
                    var duration = data.task_list[i].duration;
                    var key = data.task_list[i].key;
                    var done = data.task_list[i].done;
                    var isPrivate = data.task_list[i].isPrivate;
                    var timestamp = data.task_list[i].timestamp.substring(0,10);


                        if(isPrivate) {
                            privateField = "private";
                        }

                    $("#tasks").append("<li id='tasktable' class='row " + privateField + "' value='" + key + "'>" +
                            "<div class='description'>" + description + "</div> <div class='attributes'>" + 
                            /*"<div class='isPrivate'>" + isPrivate + " </div>" + */
                            "<div class='duration'>" + duration + " minutes </div>" + 
                            "<div class='timestamp'>" + timestamp + "</div> </div></li>");
                }
            });
}

// This is used for main page
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
                    console.log(data.task_list[i].done )
                    if (data.task_list[i].done == true || data.task_list[i].done == 'true') {
                        var done = "done"
                    } else {
                        var done = 'not done'; 
                    }
                    var isPrivate = data.task_list[i].isPrivate;
                    var timestamp = data.task_list[i].timestamp.substring(0,10);

                    var privateField = "public";

                        if(isPrivate) {
                            privateField = "private";
                        }

                    $("#tasks").append("<li class='finishTask' onclick='onFinishClicked(event)' class='row " + privateField + "' value='" + key + "'>" +
                            "<div class='description'>" + description + "</div> <div class='attributes'>" + 
                            "<div class='done'>" + done + " </div>" + 
                            /*"<div class='isPrivate'>" + isPrivate + " </div>" + */
                            "<div class='duration'>" + duration + " minutes </div>" + 
                            "<div class='timestamp'>" + timestamp + "</div> </div></li>" + 
                            "<a class='deleteButton' onclick='onDeleteClicked(event)' data-key=\"" + key + "\" style='position:relative; top: -30px; left:280; margin-left:300px; font-size:20px' name=" + key + ">X</a>");
                }
            });
}
