/*

Copyright 2011, Google Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

 * Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above
copyright notice, this list of conditions and the following disclaimer
in the documentation and/or other materials provided with the
distribution.
 * Neither the name of Google Inc. nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,           
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY           
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

 */

Refine.OpenProjectUI = function(elmt) {
  var self = this;

  elmt.html(DOM.loadHTML("core", "scripts/index/open-project-ui.html"));

  this._elmt = elmt;
  this._elmts = DOM.bind(elmt);

  $("#project-file-input").change(function() {
    if ($("#project-name-input")[0].value.length === 0) {
      var fileName = this.files[0].fileName;
      if (fileName) {
        $("#project-name-input")[0].value = fileName.replace(/\.\w+/, "").replace(/[_\-]/g, " ");
      }
      $("#project-name-input").focus().select();
    }
  }).keypress(function(evt) {
    if (evt.keyCode == 13) {
      return self._onClickUploadFileButton(evt);
    }
  });

  $("#upload-file-button").click(function(evt) {
    return self._onClickUploadFileButton(evt);
  });

  $('#projects-workspace-open').text($.i18n._('core-index-open')["browse"]);
  $('#projects-workspace-open').click(function() {
    $.ajax({
      type: "POST",
      url: "command/core/open-workspace-dir",
      dataType: "json",
      success: function (data) {
        if (data.code != "ok" && "message" in data) {
          alert(data.message);
        }
      }
    });
  });

  this._fetchProjects();
};

  Refine.OpenProjectUI.prototype.resize = function() {
  var height = this._elmt.height();
  var width = this._elmt.width();
  //var controlsHeight = this._elmts.workspaceControls.outerHeight();

  this._elmts.projectsContainer
  .css("height", (height /*- controlsHeight*/ - DOM.getVPaddings(this._elmts.projectsContainer)) + "px");

 /* this._elmts.workspaceControls
  .css("bottom", "0px")
  .css("width", (width - DOM.getHPaddings(this._elmts.workspaceControls)) + "px");*/
};

Refine.OpenProjectUI.prototype._fetchProjects = function() {
  var self = this;
  $.getJSON(
      "command/core/get-all-project-metadata",
      null,
      function(data) {
        self._renderProjects(data);
        self.resize();
      },
      "json"
  );
};

Refine.OpenProjectUI.prototype._renderProjects = function(data) {
  var self = this;
  var projects = [];
  for (var n in data.projects) {
    if (data.projects.hasOwnProperty(n)) {
      var project = data.projects[n];
      project.id = n;
      project.date = moment(project.modified).format('YYYY-MM-DD HH:mm A');
      
      if (typeof project.userMetadata !== "undefined")  {
          for (var m in data.customMetadataColumns) {
              var found = false;
              for(var i = 0; i < project.userMetadata.length; i++) {
                  if (project.userMetadata[i].name === data.customMetadataColumns[m].name) {
                      found = true;
                      break;
                  }
                  if (!found) {
                      project.userMetadata.push({
                          name: data.customMetadataColumns[m].name,
                          dispay: data.customMetadataColumns[m].display,
                          value: ""
                      });
                  }
              }
          }
      }
    }
    projects.push(project);
  }

  var container = $("#projects-container").empty();
  if (!projects.length) {
    $("#no-project-message").clone().show().appendTo(container);
  } else {
    Refine.selectActionArea('open-project');

    var table = $(
      '<table class="tablesorter-blue list-table"><thead><tr>' +
      '<th></th>' +
      '<th></th>' +
        // TODO: table headers
      '<th>'+$.i18n._('core-index-open')["last-mod"]+'</th>' +
      '<th>'+$.i18n._('core-index-open')["name"]+'</th>' +
      '<th>'+$.i18n._('core-index-open')["creator"]+'</th>' +
      '<th>'+$.i18n._('core-index-open')["subject"]+'</th>' +
      '<th>'+$.i18n._('core-index-open')["description"]+'</th>' +
      '<th>'+$.i18n._('core-index-open')["row-count"]+'</th>' + 
      (function() {
          var htmlDisplay = "";
          for (var n in data.customMetadataColumns) {
            if (data.customMetadataColumns[n].display) {
              htmlDisplay += '<th>'+ data.customMetadataColumns[n].name + '</th>';
            }
          }
          
          return htmlDisplay;
      })() +     
      '</tr></thead><tbody></tbody></table>'
    ).appendTo(container)[0];

    var renderProject = function(project) {
      var tr = table.getElementsByTagName('tbody')[0].insertRow(table.rows.length - 1);
      tr.className = "project";

      var deleteLink = $('<a></a>')
      .addClass("delete-project btn btn-link text-muted")
      .attr("title",$.i18n._('core-index-open')["del-title"])
      .attr("href","")
      .html("<i class='icon-trash'/>")
      .click(function() {
        if (window.confirm($.i18n._('core-index-open')["del-body"] + project.name + "\"?")) {
          $.ajax({
            type: "POST",
            url: "command/core/delete-project",
            data: { "project" : project.id },
            dataType: "json",
            success: function (data) {
              if (data && typeof data.code != 'undefined' && data.code == "ok") {
                self._fetchProjects();
              }
            }
          });
        }
        return false;
      }).appendTo(
        $(tr.insertCell(tr.cells.length))
      );

      var editMetadataLink = $('<a></a>')
      .html("<i class='icon-info'/>")
      .addClass("btn btn-link text-primary")
      .attr("href", "javascript:{}")
      .attr("title", "Show metadata")
      .click(function() {
          new EditMetadataDialog(project, $(this).parent().parent());
      })
      .appendTo(
        $(tr.insertCell(tr.cells.length))
      );
      
      $('<div></div>')
      .html(project.date)
      .addClass("last-modified")
      .appendTo($(tr.insertCell(tr.cells.length)));
      
      var nameLink = $('<a></a>')
      .addClass("project-name")
      .text(project.name)
      .attr("href", "project?project=" + project.id)
      .appendTo($(tr.insertCell(tr.cells.length)));
      
      var appendMetaField = function(data) {
          $('<div></div>')
          .html(data)
          .appendTo($(tr.insertCell(tr.cells.length)));
      };
      
      appendMetaField(project.creator);
      appendMetaField(project.subject);
      appendMetaField(project.description, '20%');
      appendMetaField(project.rowCount);
      
      var data = project.userMetadata;
      for(var i in data)
      {
           if (data[i].display === true) {
               appendMetaField(data[i].value); 
           }
      }
    };

    for (var i = 0; i < projects.length; i++) {
      renderProject(projects[i]);
    }

    $(table).tablesorter({
        headers : {
            0: { sorter: false },
            1: { sorter: false },
            2: { sorter: "text" }
        },
        sortList: [[2,1]],
        widthFixed: false
    });
  }
};

Refine.OpenProjectUI.prototype._onClickUploadFileButton = function(evt) {
  var projectName = $("#project-name-input")[0].value;
  var dataURL = $.trim($("#project-url-input")[0].value);
  if (! $.trim(projectName).length) {
    window.alert($.i18n._('core-index-open')["warning-proj-name"]);

  } else if ($("#project-file-input")[0].files.length === 0 && ! dataURL.length) {
    window.alert($.i18n._('core-index-open')["warning-data-file"]);

  } else {
    $("#file-upload-form").attr("action",
        "command/core/create-project-from-upload?" + [
          "url=" +                encodeURIComponent(dataURL),
          "split-into-columns=" + $("#split-into-columns-input")[0].checked,
          "separator=" +          $("#separator-input")[0].value,
          "ignore=" +             $("#ignore-input")[0].value,
          "header-lines=" +       $("#header-lines-input")[0].value,
          "skip=" +               $("#skip-input")[0].value,
          "limit=" +              $("#limit-input")[0].value,
          "guess-value-type=" +   $("#guess-value-type-input")[0].checked,
          "ignore-quotes=" +      $("#ignore-quotes-input")[0].checked,
          // Ontotext: appends auth token as URI param
          "authToken=" +          encodeURIComponent(getGraphDBAuthToken())
        ].join("&"));

    return true;
  }

  evt.preventDefault();
  return false;
};

Refine.OpenProjectUI.refreshProject = function(tr, metaData) {
    var refreshMetaField = function(data, index) {
        if (index === 3) {
            $('a', $('td', tr).eq(index))
            .text(data);
        } else {
            $('td', tr).eq(index)
            .text(data);
        }
    };
    
    var index = 3;
    refreshMetaField(metaData.name, index); index++;
    refreshMetaField(metaData.creator, index); index++;
    refreshMetaField(metaData.subject,index); index++;
    refreshMetaField(metaData.description,index); index++;
    refreshMetaField(metaData.rowCount,index); index++;
    
    var updateUserMetadata = function(ob) {
        var userMetadata = ob.userMetadata;
        
        for ( var n in ob) {
            for ( var i in userMetadata) {
                if (n === userMetadata[i].name) {
                    userMetadata[i].value = ob[n];
                    break;
                }
            }
        }
        
        ob.userMetadata = userMetadata;
    };
    updateUserMetadata(metaData);
    var data = metaData.userMetadata;
    for(var i in data)
    {
         if (data[i].display === true) {
             refreshMetaField(data[i].value,index); index++; 
         }
    }

};

Refine.actionAreas.push({
  id: "open-project",
  label: $.i18n._('core-index-open')["open-proj"],
  uiClass: Refine.OpenProjectUI
});
