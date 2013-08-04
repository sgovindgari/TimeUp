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

    //$(".tasklist li").click(finishitem($(this).attr("value")));

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
      
       function deleteTask(value){
            var key = value;
            $.post("/deletetask", function(data){
                getTasks();
            });
        }
      
      $("#deleteButton").click(function(){
        var value = $(this).attr("name");
        deleteTask(value);
      });       
      
          function finishitem(id) {
          $.post("/tasks", {"id":id}, function(data) { 
            console.log(data);
            getTasks(); 
            });
            }

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
                  var timestamp = data.task_list[i].timestamp.substring(0,10);

                  var privateField = "public";
                  var done = "not done"

                    if(isPrivate) {
                      privateField = "private";
                    }

                  $("#tasks").append("<li id='tasktable' class='row " + privateField + "' value='" + key + "'>" +
                      "<div class='description'>" + description + "</div> <div class='attributes'>" + 
                      "<div class='done'>" + done + " </div>" + 
                      /*"<div class='isPrivate'>" + isPrivate + " </div>" + */
                      "<div class='duration'>" + duration + " minutes </div>" + 
                      "<div class='timestamp'>" + timestamp + "</div> </div>" + 
                      "<button id='deleteButton' style='margin-left:300px; font-size:20px' name=" + key + ">X</button></li>");
                }
                });
          }
        });
