import {
    VisualController
} from '../controller/VisualController';
import Konva from 'konva';

var visualController = new VisualController();

class EditStudyView {
    constructor() {
        this.stage = null;
        this.navigation = document.getElementById("navigation");
        this.toolboxPane = document.getElementById("toolboxPane");
        this.specificationPane = document.getElementById("specificationPane");
        this.stageParent = document.getElementById("stage-parent");
        this.containerDOM = document.getElementById("container");
        this.selectionButton = document.getElementById("selectionButton");
        this.conductorButton = document.getElementById("conductorButton");
        this.clientButton = document.getElementById("clientButton");
        this.resetButton = document.getElementById("resetButton");
        this.zoomInButton = document.getElementById("zoomInButton");
        this.zoomOutButton = document.getElementById("zoomOutButton");
        this.zoomStatus = document.getElementById("zoomStatus");
        this.message = document.getElementById("message");
        this.positionInfo = document.getElementById("positionInfo");
        this.conductorContextMenu = document.getElementById("conductor"); //Button when right click (conductor)
        this.transfoContextMenu = document.getElementById("transfo"); //Button when right click (transfo)
        this.clientContextMenu = document.getElementById("client"); //Button when right click (client)
        this.menuDisplayed = false;
        this.menuBox = null;
        this.windowDOM = window;
        this.initVisual();
        this.initEvents();
    }

    initVisual() {
        //TODO Call Visual Controller
        visualController.initVisual(undefined, this.containerDOM);

    }

    initEvents() {
        this.containerDOM.addEventListener("click", function(event) {
            var isDraggable = document.getElementById("drag");
            var isCreating = document.getElementById("create");


            // Model from CanvaController
            if (visualController.getCreateLine() == true) {
                visualController.handleGenerateConductor(event);
                // generateConductor(event);
            } else if (visualController.getCreateTransfo() == true) {
                visualController.handleGenerateTransformer(event);
                // generateTranformer(event);
            } else if (visualController.getCreateClient() == true) {
                visualController.handleGenerateClient(event);
                // generateClient(event);
            }
        });



        window.addEventListener("contextmenu", function(event) {
            var left = event.x;
            var top = event.y;

            this.menuBox = window.document.querySelector(".menu");
            this.menuBox.style.left = left + "px";
            this.menuBox.style.top = top + "px";
            this.menuBox.style.display = "block";

            event.preventDefault();

            this.menuDisplayed = true;
        }, false);

        window.addEventListener("click", function() {
            if (this.menuDisplayed == true) {
                menuBox.style.display = "none";
            }
        });

        //Zoom in button
        this.zoomInButton.addEventListener("click", function() {

            if (this.zoomLevel == 1) {
                this.originalLayerPositionX = this.currentLayerPositionX;
                this.originalLayerPositionY = this.currentLayerPositionY
            }

            if (this.zoomLevel <= this.zoomInLimit) {
                this.zoomLevel += this.zoomStep;

                this.stage.scale({
                    x: this.zoomLevel,
                    y: this.zoomLevel
                });


                this.currentLayerPositionX = this.originalLayerPositionX / this.zoomLevel;
                this.currentLayerPositionY = this.originalLayerPositionY / this.zoomLevel;

                //Debug position code
                // var node = new Konva.Circle({
                //     x : currentLayerPositionX,
                //     y : currentLayerPositionY,
                //     radius : 30,
                //     fill : 'red',
                //     stroke: 'black',
                //     strokeWidth : 2,
                //     id : "N" + nodeIdNumber
                // });

                // layer.add(node);
                // layer.draw();

                var status = parseInt(zoomLevel * 100); //Make sure that status is an integer

                this.zoomStatus.innerHTML = status + "%";
            }
            if (this.zoomLevel == 1) {
                this.currentLayerPositionX = this.originalLayerPositionX;
                this.currentLayerPositionY = this.originalLayerPositionY;
            }

            this.stage.draw();
        });


        //Deal with the events when clicking the zoom in button
        this.zoomOutButton.addEventListener("click", function() {

            if (this.zoomLevel == 1) {
                this.originalLayerPositionX = this.currentLayerPositionX;
                this.originalLayerPositionY = this.currentLayerPositionY;
            }

            if (this.zoomLevel > this.zoomStep) {
                this.zoomLevel -= this.zoomStep;
                this.stage.scale({
                    x: this.zoomLevel,
                    y: this.zoomLevel
                });

                this.currentLayerPositionX = (this.originalLayerPositionX / this.zoomLevel);
                this.currentLayerPositionY = (this.originalLayerPositionY / this.zoomLevel);

                // Debug Position Code
                // console.log({X : currentLayerPositionX, Y : currentLayerPositionY});
                // var node = new Konva.Circle({
                //     x : currentLayerPositionX,
                //     y : currentLayerPositionY,
                //     radius : 30,
                //     fill : 'red',
                //     stroke: 'black',
                //     strokeWidth : 2,
                //     id : "N" + nodeIdNumber
                // });

                // layer.add(node);
                // layer.draw();


                var status = parseInt(zoomLevel * 100); //Make sure that status is an integer

                this.zoomStatus.innerHTML = status + "%";
            }

            if (this.zoomLevel == 1) {
                this.currentLayerPositionX = this.originalLayerPositionX;
                this.currentLayerPositionY = this.originalLayerPositionY;
            }

            this.stage.draw();
        });
        this.conductorContextMenu.addEventListener("click", function() {
            if (this.menuDisplayed == true) {
                selectConductor();
            }
        });

        // transfoContextMenu.addEventListener("click", function(){
        //     if(menuDisplayed == true){
        //         selectTranformer();
        //     }
        // });

        //Not working yet To test later
        this.clientContextMenu.addEventListener("click", function() {
            if (menuDisplayed == true) {
                selectClient(); // ToolBoxModel -> Handled by CanvaController -> VisualController
            }
        });

        // transformerButton.addEventListener("click", function(){
        //     selectTranformer();
        // });

        //Not working yet To test later
        this.clientButton.addEventListener("click", function() {
            visualController.setClientVisual();
            //selectClient(); // ToolBoxModel -> Handled by CanvaController -> VisualController
        })

        this.conductorButton.addEventListener("click", function() {
            visualController.setConductorVisual();
            //selectConductor(); // ToolBoxModel -> Handled by CanvaController -> VisualController
        });

        this.selectionButton.addEventListener("click", function() {
            visualController.setSelectToolVisual();
            //selectSelectTool(); // ToolBoxModel -> Handled by CanvaController -> VisualController
        });

        // this.stage.addEventListener("dragstart", function(){
        //     layerStartDrag = stage.getPointerPosition(); // CanvaModel -> CanvaController -> VisualController
        // });
        //
        // this.stage.addEventListener("dragmove", function(){
        //     // var pos = stage.getPointerPosition();
        //     // currentPosition.x += ( - (pos.x - layerStartDrag.x) );
        //     // currentPosition.y += ( - (pos.y - layerStartDrag.y) );
        //     // positionInfo.innerHTML = JSON.stringify(currentPosition);
        // });
        //
        // this.stage.addEventListener("dragend", function(){
        //     var layerEndDrag = stage.getPointerPosition();
        //
        //     var distanceX = (layerEndDrag.x - this.layerStartDrag.x);
        //     var distanceY = (layerEndDrag.y - this.layerStartDrag.y);
        //
        //     this.currentLayerPositionX += ( - this.distanceX ) /this.zoomLevel; //brings you position of current origin *1
        //     this.currentLayerPositionY += ( - this.distanceY ) / this.zoomLevel; //brings you position of current origin *1
        //     //*1 CanvaModel -> CanvaController -> VisualController
        //     if(this.zoomLevel != 1){
        //         this.originalLayerPositionX += ( - distanceX ); // CanvaModel -> CanvaController -> VisualController
        //         this.originalLayerPositionY += ( - distanceY );// CanvaModel -> CanvaController -> VisualController
        //     }
        //     currentPosition.x = this.currentLayerPositionX; // CanvaModel -> CanvaController -> VisualController
        //     currentPosition.y = this.currentLayerPositionY;// CanvaModel -> CanvaController -> VisualController
        //     this.positionInfo.innerHTML = JSON.stringify(this.currentPosition);
        //     // handlePointerConstraint();
        // });

        this.containerDOM.addEventListener("scroll", function(event) {
            event.preventDefault();

            console.log(event);

        });

        this.resetButton.addEventListener("click", function() {
            stage.x(0);
            stage.y(0);

            this.currentLayerPositionX = 0;
            this.currentLayerPositionY = 0;

            this.originalLayerPositionX = 0;
            this.originalLayerPositionY = 0;

            setPositionInfoToZero();

            this.stage.draw();
        });
        $('#voltageSelection').change(function(event) {
            var csrf_token = $('.voltageBox input[type="hidden"]').val();
            var study_voltage = $('#voltageSelection').val();
            $.ajax({
                url: "get_type_possible_information/" + study_voltage,
                method: "GET",
                headers: {
                    "X-CSRFToken": csrf_token,
                    "Application-Type": "application/json"
                },
                success: function(response) {
                    console.log(response)
                    var transformerType = $('#transformerTypeList');
                    transformerType.empty();
                    transformerType.append($('<option></option>').attr('value', 'None').text(" ---- "));
                    $.each(response.type_transformateur, function(key, value) {
                        json_data = JSON.parse(value);
                        transformerType.append($('<option></option>')
                            .attr("value", json_data.type_transformateur_id)
                            .text(json_data.type_transformateur_type));
                    });

                    var conductorType = $('#conductorTypeList');
                    conductorType.empty();
                    conductorType.append($('<option></option>').attr('value', 'None').text(' ---- '));
                    $.each(response.type_conducteur, function(key, value) {
                        json_data = JSON.parse(value);
                        conductorType.append($('<option></option')
                            .attr("value", json_data.type_conducteur_id)
                            .text(json_data.type_conducteur_type));
                    });
                },
                error: function(response) {
                    alert('Fail')
                }
            });
        });

        /*
          Component caracteristic changes
        */
        $("#conductor_length").change(function(event) {
            elementChanged = $("#elementName").html();
            elementChanged = elementChanged.replace("Conducteur :", "");
            elementChanged = elementChanged.trim();
            for (let i = 0; i < componentListBuffer.length; i++) {
                if (componentListBuffer[i].nom_du_noeud == elementChanged) {
                    componentListBuffer[i].longueur = parseInt(event.target.value);
                }
            }
        });

        function extractNodeFromHTML(htmlString) {
            htmlString = htmlString.replace("Client :", "");
            htmlString = htmlString.trim();
            return htmlString;
        }

        $("#habitable_area").change(function(event) {
            elementChanged = extractNodeFromHTML($("#elementName").html());
            for (let i = 0; i < componentListBuffer.length; i++) {
                if (componentListBuffer[i].nom_du_noeud == elementChanged) {
                    componentListBuffer[i].surface_habitable = parseInt(event.target.value);
                }
            }
        });

        $("#number_of_floors").change(function(event) {
            elementChanged = extractNodeFromHTML($("#elementName").html());
            for (let i = 0; i < componentListBuffer.length; i++) {
                if (componentListBuffer[i].nom_du_noeud == elementChanged) {
                    componentListBuffer[i].nombre_etage = parseInt(event.target.value);
                }
            }
        });

        $("#number_of_lodgings").change(function(event) {
            elementChanged = extractNodeFromHTML($("#elementName").html());
            for (let i = 0; i < componentListBuffer.length; i++) {
                if (componentListBuffer[i].nom_du_noeud == elementChanged) {
                    componentListBuffer[i].nombre_de_logement = parseInt(event.target.value);
                }
            }
        });

        /*
          Computing handling part of the code
        */

        $("#calculate_network").click(function(event) {
            var csrf_token = $('.voltageBox input[type="hidden"]').val();
            $.ajax({
                url: "get_compute_network",
                type: "POST",
                data: JSON.stringify(componentListBuffer),
                headers: {
                    "X-CSRFToken": csrf_token,
                    "Application-Type": "application/json"
                },
                success: function(computed_values) {
                    console.log(computed_values.data);
                    $("#log").html(computed_values.data);
                },
                error: function(error) {
                    alert("Erreur");
                }
            })
        });
    }
}

export {
    EditStudyView
}