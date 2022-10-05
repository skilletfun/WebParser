import QtQuick 2.15
import QtQuick.Controls 2.15


Popup {
    id: root

    property bool download: false

    modal: true
    closePolicy: Popup.NoAutoClose

    background: Rectangle { radius: 15; border.width: 1; color: color_base }

    enter: Transition {
        NumberAnimation { property: 'opacity'; from: 0; to: 1; duration: 200 }
    }

    exit: Transition {
        NumberAnimation { property: 'opacity'; from: 1; to: 0; duration: 200 }
    }

    onOpened: {
        root.start_download();
    }

//-----------------------------------------  Timer request from python statistic ---------------------//

    Timer {
        id: timer_animate

        property bool allowed: true
        property bool flag: true

        interval: 250
        repeat: true

        onTriggered: {
            root.check_state();
        }
    }
//-------------  Upper line ----------//

    Rectangle {
        width: parent.width * 0.9
        height: 1
        anchors.horizontalCenter: border_download.horizontalCenter
        anchors.bottom: border_download.top
        anchors.bottomMargin: 5
        color: "black"
    }

//---------------   Invisible rect with ListView  -------------//

    Rectangle {
        id: border_download
        radius: 12
        anchors.fill: parent
        anchors.margins: 50
        anchors.bottomMargin: 100
        color: 'transparent'

        ListView {
            id: chapter_download_list
            model: chapter_download_model
            spacing: 5
            clip: true
            anchors.fill: parent
            anchors.margins: 20

            add: Transition {
                NumberAnimation { properties: "opacity"; from: 0; to: 1; duration: 300 }
            }

            delegate: Rectangle {
                height: 85
                width: chapter_download_list.width
                color: 'white'
                border.color: 'grey'
                radius: 15
                clip: true

//-----------------------   Title of chapter  -------------------//

                Text {
                    id: lbl_title
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.margins: 10
                    text: String(current_title).slice(0, 57)
                    font.pixelSize: 20
                    font.bold: true
                    font.family: 'Arial'
                }

//------------------------  Count of downloaded images by all --------------//

                Text {
                    id: lbl_images
                    anchors.left: parent.left
                    anchors.top: lbl_title.bottom
                    anchors.leftMargin: 10
                    anchors.topMargin: 1
                    text: 'Images: ' + total_download_images + ' / ' + total_images
                    font.pixelSize: 15
                    font.family: 'Arial'
                }
//------------------------  Progress in percent %  --------------//

                Text {
                    id: lbl_progress
                    anchors.left: parent.left
                    anchors.top: lbl_images.bottom
                    anchors.leftMargin: 10
                    text: 'Status: ' + String(Math.floor(Number(total_download_images) * 100 / Number(total_images))) + ' %'
                    font.pixelSize: 15
                    font.family: 'Arial'
                }

//------------------------  Rectanle animated --------------//

                Rectangle {
                    height: parent.height - 2
                    width: height
                    clip: true
                    color: parent.color
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.rightMargin: 20

                    Rectangle {
                        id: anim_rect
                        anchors.fill: parent
                        clip: true
                        color: parent.color
                        radius: height / 2

                        Rectangle {
                            anchors.fill: parent
                            anchors.margins: 15
                            color: 'grey'
                            radius: height / 2

                            Rectangle {
                                anchors.fill: parent
                                anchors.margins: 5
                                color: 'white'
                                radius: height / 2
                            }
                        }

                        Rectangle {
                            color: parent.color
                            height: parent.height
                            width: parent.width/2
                            anchors.top: parent.top
                            anchors.right: parent.horizontalCenter
                        }

                        Rectangle {
                            color: parent.color
                            height: parent.height/2
                            width: parent.width
                            anchors.top: parent.top
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                    }

                    Rectangle {
                        id: rect_checked
                        opacity: 0
                        anchors.fill: parent
                        clip: true
                        radius: height / 2
                        anchors.margins: 15
                        color: 'grey'

                        Rectangle {
                            anchors.fill: parent
                            anchors.margins: 3
                            color: 'white'
                            radius: height / 2
                        }

                        Rectangle {
                            color: 'grey'
                            width: 3
                            transformOrigin: Item.TopLeft
                            height: parent.height / 3
                            anchors.horizontalCenter: parent.horizontalCenter
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.verticalCenterOffset: 20
                            rotation: 135
                        }

                        Rectangle {
                            color: 'grey'
                            width: 3
                            height: parent.height / 2
                            transformOrigin: Item.TopLeft
                            anchors.horizontalCenter: parent.horizontalCenter
                            anchors.horizontalCenterOffset: -1
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.verticalCenterOffset: 26
                            rotation: 225
                        }
                    }
                }

                PropertyAnimation {
                    id: anim_1
                    target: anim_rect
                    running: root.download && index == chapter_download_model.count - 1
                    property: 'rotation'
                    duration: 750
                    from: 0
                    to: 360
                    loops: Animation.Infinite
                }

                SequentialAnimation {
                    running: !anim_1.running
                    loops: 1

                    PropertyAnimation {
                        target: rect_checked
                        property: 'opacity'
                        duration: 150
                        from: 0
                        to: 1
                    }
                }
            }
//------------------------  End of Rectange Animated --------------//

            ListModel {
                id: chapter_download_model
                onCountChanged: { chapter_download_list.positionViewAtEnd(); }
            }
        }
    }

//------------------------  Line at the bottom  --------------//

    Rectangle {
        width: parent.width * 0.9
        height: 1
        anchors.horizontalCenter: border_download.horizontalCenter
        anchors.top: border_download.bottom
        anchors.topMargin: 5
        color: "black"
    }

//------------------------  Statistic by right from Cancel\Ok button --------------//

    Column {
        anchors.verticalCenter: cancel_apply_download.verticalCenter
        anchors.left: cancel_apply_download.right
        anchors.leftMargin: 150

        Text {
            text: 'Total chapters: ' + String(chapter_download_model.count)
            font.pixelSize: 16
            font.family: 'Arial'
        }

        Text {
            id: total_images_label
            property int total_imgs: 0
            text: 'Total images: ' + String(total_imgs)
            font.pixelSize: 16
            font.family: 'Arial'
        }
    }

//------------------------  Cancel\Ok Button  ------------------------//

    Button {
        id: cancel_apply_download

        width: 150
        height: 50

        text: root.download ? "Cancel" : "Ok"
        font.pixelSize: height / 2

        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 25

        background: Rectangle { radius: 10; border.width: 1; color: cancel_apply_download.pressed ?
             color_press : cancel_apply_download.hovered ? color_hover : 'white'; }

        onReleased: {
            root.close();
            root.download = false;
            parser.cancel_download();
        }
    }

    function start_download()
    {
        root.download = true;
        total_images_label.total_imgs = 0;
        chapter_download_model.clear();
        timer_animate.start();
        timer_animate.allowed = true;
        timer_animate.flag = true;
    }

    function check_state()
    {
        if (timer_animate.allowed)
        {
            var current_title = String(parser.get_current_title());
            var total_images = String(parser.get_total_images());
            var total_download_images = String(parser.get_total_download_images());

            if (current_title !== '' && total_images !== '0')
            {
                if (chapter_download_model.count === 0)
                {
                    chapter_download_model.append({'current_title': current_title,
                                                      'total_images': total_images,
                                                      'total_download_images': total_download_images});
                }
                else if (chapter_download_model.get(chapter_download_model.count-1).current_title === current_title)
                {
                    chapter_download_model.setProperty(chapter_download_model.count-1, 'total_download_images', total_download_images);
                }
                else
                {
                    chapter_download_model.append({'current_title': current_title,
                                                      'total_images': total_images,
                                                      'total_download_images': total_download_images});
                }
            }
            root.update_total_img();
        }
        if (parser.get_running() === 'True') timer_animate.allowed = true;
        else if (timer_animate.flag)
        {
            timer_animate.flag = false;
            timer_animate.allowed = true;
        }
        else
        {
            timer_animate.allowed = false;
            root.download = false;
            timer_animate.stop();
        }
    }

    function update_total_img()
    {
        total_images_label.total_imgs = 0;
        for (var i = 0; i < chapter_download_model.count; i++)
        {
            total_images_label.total_imgs += Number(chapter_download_model.get(i).total_download_images);
        }
}

}
