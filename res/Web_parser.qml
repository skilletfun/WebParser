import QtQuick 2.15
import QtQuick.Controls 2.12
import QtQuick.Window 2.12

Window {
    id: root

// ---------------------- Colors -------------------------//

    property color color_base: "#EEFFFF"
    property color color_accent: "#f0f4f2"
    property color color_hover: "#F6F6F6"
    property color color_press: "#E8E8E8"
    property color color_select: 'white'

// ------------------ Window Settings -------------------- //

    width: 900
    height: 600

    minimumHeight: 600
    minimumWidth: 900
    maximumHeight: 600
    maximumWidth: 900

    title: "WebParser"
    visible: true
    color: color_base

// ----------------------------  Title ----------------------------//
    Header {
        anchors.fill: parent
    }

// ----------------------------  Settings Button  ----------------------------//
    Button {
        id: settings

        height: 60
        width: height

        anchors.right: parent.right
        anchors.top: parent.top
        anchors.rightMargin: 25
        anchors.topMargin: 25

        background: Rectangle { radius: height / 2;
            color: settings.pressed ? color_press : settings.hovered ? 'white' : 'transparent'; }

        icon.source: "gear.png"
        icon.color: 'transparent'
        icon.width: width * 0.9
        icon.height: width * 0.9

        onReleased: { settings_popup.open(); }
    }

// ----------------------------  Settings Popup Main  ----------------------------//

    SettingsPopup {
        id: settings_popup

        height: parent.height * 0.98
        width: parent.width * 0.98
        anchors.centerIn: parent

    }

// ---------------------------- Additional Settings ----------------------------//

    AddSettings {
        id: add_settings

        width: 200
        height: 300
        radius: 30
        x: 45
        y: 150
    }

    RedownloadPopup {
        id: redownload_images_popup
        anchors.centerIn: parent
    }

//---------------------------------- Settings Url----------------------------------------------//

    UrlSettings {
        id: url_settings
        width: 575
        height: 300
        x: 280
        y: 150
    }

//----------------------------------- Button PARSE ----------------------------------------------//

    Button {
        id: startParse

        enabled: url_settings.url != ''

        width: 150
        height: 50

        text: "Parse"
        font.pixelSize: height / 2

        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.margins: 50

        background: Rectangle { radius: 5; border.width: 1;
            color: startParse.pressed ? color_press : startParse.hovered ? color_hover : 'white'; }

        onReleased: {
            parser.parse(url_settings.url, add_settings.timeout, url_settings.folder,
                redownload_images_popup.redownload, add_settings.archive, add_settings.merge, url_settings.count_of_chapters);
            download_popup.open();
        }
    }

//---------------------------------- Popup Animation Download ----------------------------------------------//

    Popup {
        id: download_popup

        property bool download: false

        width: parent.width * 0.95
        height: parent.height * 0.95
        modal: true

        anchors.centerIn: parent
        closePolicy: Popup.NoAutoClose

        background: Rectangle { radius: 15; border.width: 1; color: root.color_base }

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
                        running: download_popup.download && index == chapter_download_model.count - 1
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

            text: download_popup.download ? "Cancel" : "Ok"
            font.pixelSize: height / 2

            anchors.bottom: parent.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottomMargin: 25

            background: Rectangle { radius: 10; border.width: 1; color: cancel_apply_download.pressed ?
                 color_press : cancel_apply_download.hovered ? color_hover : 'white'; }

            onReleased: {
                download_popup.close();
                download_popup.download = false;
                parser.cancel_download();
            }
        }
    }

    function start_download()
    {
        download_popup.download = true;
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
            download_popup.download = false;
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




