import QtQuick 2.15
import QtQuick.Controls 2.12
import QtQuick.Shapes 1.12
import Qt.labs.platform 1.0
import QtQuick.Window 2.12

Window {
    id: root

// ---------------- Colors ------------------//

    property color color_base: "#EEFFFF"
    property color color_accent: "#278cff"
    property color color_hover: "#F6F6F6"
    property color color_press: "#E8E8E8"

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

// ---------------  Title -------------------- //

    Text {
        id: title
        text: 'WebParser v1.1'
        font.pixelSize: 32
        font.bold: true
        font.family: 'Arial'
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 45
        anchors.topMargin: 30
    }

    Text {
        id: help_title
        text: 'Support 8 sites'
        font.pixelSize: 16
        font.family: 'Arial'
        anchors.left: parent.left
        anchors.top: title.bottom
        anchors.leftMargin: 45
        anchors.topMargin: 10
    }

    Button {
        id: help_title_btn
        height: 20
        width: height

        background: Rectangle { radius: help_title_btn.height/2; border.color: 'black';
            color: help_title_btn.pressed ? color_press : help_title_btn.hovered ? color_hover : 'white'; }

        anchors.verticalCenter: help_title.verticalCenter
        anchors.left: help_title.right
        anchors.leftMargin: 20
        text: '?'

        onReleased: {
            help_title_popup.open();
        }
    }

    Popup {
        id: help_title_popup
        width: parent.width/3
        height: parent.height / 1.2

        background: Rectangle { border.color: "black"; radius: 15 }
        modal: true

        enter: Transition {
            NumberAnimation { property: 'opacity'; from: 0; to: 1; duration: 200 }
        }

        exit: Transition {
            NumberAnimation { property: 'opacity'; from: 1; to: 0; duration: 200 }
        }

        anchors.centerIn: parent

        ListView {
            id: list_sites
            clip: true
            model: model_sites
            anchors.fill: parent
            anchors.leftMargin: 10
            anchors.topMargin: 10
            spacing: 15

            delegate: Text {
                text: _text
                font.pixelSize: 16
                font.family: 'Arial'
            }
        }

        ListModel {
            id: model_sites
            ListElement {
                _text: 'fanfox.net'
            }
            ListElement {
                _text: 'manhuadb.com'
            }
            ListElement {
                _text: 'manga.bilibili.com'
            }
            ListElement {
                _text: 'mangareader.to'
            }
            ListElement {
                _text: 'rawdevart.com'
            }
            ListElement {
                _text: 'webmota.com (baozihm.com)'
            }
            ListElement {
                _text: 'webtoons.com'
            }
            ListElement {
                _text: 'page.kakao.com'
            }
        }
    }

//------------------------ End of titles --------------------------//



// ---------------------------- Additional Settings ----------------------------//

    Rectangle {
        id: add_settings_rect
        width: 200
        height: 300
        radius: 30
        border.color: "black"
        x: 45
        y: 150

// --------------------- Title ------------------------//

        Text {
            id: title_add_settings
            text: 'Add. settings'
            font.family: 'Arial'
            font.pixelSize: 18
            font.italic: true
            y: 20
            anchors.horizontalCenter: parent.horizontalCenter
        }

// --------------------- Archive ------------------------//

        CheckBox {
            id: do_archive
            text: 'Archive'
            font.pixelSize: 16
            font.family: 'Arial'
            anchors.left: parent.left
            anchors.top: title_add_settings.top
            anchors.leftMargin: 30
            anchors.topMargin: 40
        }

// --------------------- Download Next Chapter ------------------------//



// ---------------------- Timeout ------------------------//

        Text {
            id: timeout_text
            text: 'Timeout: ' + String(slider_timeout.value)
            font.family: 'Arial'
            font.pixelSize: 16
            anchors.left: parent.left
            anchors.top: do_archive.top
            anchors.leftMargin: 40
            anchors.topMargin: 60
        }

// ---------------------- Timeout Slider ------------------------//

        Slider {
            id: slider_timeout
            from: 0
            to: 15
            value: 0
            stepSize: 1
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: timeout_text.top
            anchors.leftMargin: 10
            anchors.rightMargin: 10
            anchors.topMargin: 20
        }

// ---------------------- Check Chromedriver ------------------------//

        Button {
            id: check_driver
            property string status: '?'
            background: Rectangle {color: 'transparent' }
            font.family: 'Arial'
            font.pixelSize: 16
            text: 'Check driver: ' + status
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: slider_timeout.top
            anchors.topMargin: 40
            palette.buttonText: check_driver.pressed ? '#005c84' : check_driver.hovered ? '#0082B9' : 'black'

            onReleased: {
                var b = parser.check_driver();
                if (b == 'True')
                    status = 'ok';
                else
                    status = 'error';
            }
        }

//--------------------------------- Button Browser Location Settings ---------------------------//

        Button {
            id: browser_location
            background: Rectangle { color: 'transparent' }
            font.family: 'Arial'
            font.pixelSize: 16
            text: 'Chrome location'
            anchors.top: check_driver.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.topMargin: 5
            palette.buttonText: browser_location.pressed ? '#005c84' : browser_location.hovered ? '#0082B9' : 'black'

            onReleased: {
                browser_location_settings_popup.open();
            }
        }

            //--------------------------------- Button Redownloaded Images Settings ---------------------------//

        Button {
            id: redownload_images_btn
            background: Rectangle { color: 'transparent' }
            font.family: 'Arial'
            font.pixelSize: 16
            text: 'Redownload'
            anchors.top: browser_location.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.topMargin: 5
            palette.buttonText: redownload_images_btn.pressed ? '#005c84' : redownload_images_btn.hovered ? '#0082B9' : 'black'

            onReleased: {
                redownload_images_popup.open();
            }
        }
    }

//--------------------------------- Popup Browser Location Settings ---------------------------//

    Popup {
        id: browser_location_settings_popup
        width: 600
        height: 150
        anchors.centerIn: parent
        modal: true

        background: Rectangle { border.color: "black"; radius: 20 }

        enter: Transition {
            NumberAnimation { property: 'opacity'; from: 0; to: 1; duration: 200 }
        }

        exit: Transition {
            NumberAnimation { property: 'opacity'; from: 1; to: 0; duration: 200 }
        }

        Text {
            id: browser_location_text
            text: 'Path to Google Chrome Data'
            font.family: 'Arial'
            font.pixelSize: 16
            x: 45
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.margins: 15
        }

        TextField {
            id: browser_location_field
            property string path: ''
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: browser_location_text.bottom
            anchors.margins: 15
            anchors.topMargin: 10
            height: 50

            background: Rectangle { radius: 10; border.width: 1; color: browser_location_field.focus ?
                    color_press : browser_location_field.hovered ? color_hover : 'white'; }

            font.pixelSize: 18

            onAccepted: {
                focus = false;
                placeholderText = text;
                parser.set_path_to_browser(text);
            }

            onEditingFinished: {
                focus = false;
            }

            Component.onCompleted : {
                placeholderText = parser.get_path_to_browser();
            }
        }
    }


//--------------------------------- Popup Redownloaded Images Settings ---------------------------//

    Popup {
        id: redownload_images_popup
        width: 600
        height: 150
        anchors.centerIn: parent
        modal: true

        background: Rectangle { border.color: "black"; radius: 20 }

        enter: Transition {
            NumberAnimation { property: 'opacity'; from: 0; to: 1; duration: 200 }
        }

        exit: Transition {
            NumberAnimation { property: 'opacity'; from: 1; to: 0; duration: 200 }
        }

        Text {
            id: redownload_images_text
            text: 'Numbers images that should to redownload'
            font.family: 'Arial'
            font.pixelSize: 16
            x: 45
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.margins: 15
        }

        TextField {
            id: redownload_images_field
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: redownload_images_text.bottom
            anchors.margins: 15
            anchors.topMargin: 10
            height: 50

            background: Rectangle { radius: 10; border.width: 1; color: redownload_images_field.focus ?
                    color_press : redownload_images_field.hovered ? color_hover : 'white'; }

            placeholderText: '1 3 13'
            font.pixelSize: 18

            onAccepted: {
                focus = false;
            }

            onEditingFinished: {
                focus = false;
            }
        }
    }


//--------------------------------- End Additional Settings------------------------------------//


//----------------------------- Settings Url----------------------------------------------//

//----------------------------- Main Rectangle----------------------------------------------//

    Rectangle {
        id: chapter_settings_rect
        width: 575
        height: 300
        radius: 30
        border.color: "black"
        x: 280
        y: 150

//--------------------------------------- Title----------------------------------------------//

        Text {
            id: title_chapter_settings
            text: 'Chapter settings'
            font.family: 'Arial'
            font.pixelSize: 18
            font.italic: true
            y: 20
            anchors.horizontalCenter: parent.horizontalCenter
        }

//----------------------------- Label Url ----------------------------------------------//

        Text {
            id: chapter_url_text
            text: 'Url'
            font.family: 'Arial'
            font.pixelSize: 16
            x: 45
            anchors.top: title_chapter_settings.top
            anchors.topMargin: 40
        }

//----------------------------- Url Field ----------------------------------------------//

        TextField {
            id: url_field
            anchors.left: chapter_url_text.left
            anchors.top: chapter_url_text.bottom
            anchors.topMargin: 10
            height: 50
            width: 420

            background: Rectangle { radius: 10; border.width: 1; color: url_field.focus ?
                    color_press : url_field.hovered ? color_hover : 'white'; }

            placeholderText: "https://somesite.com/title/chapter/12"
            font.pixelSize: 18

            onAccepted: {
                focus = false;
            }

            onEditingFinished: {
                focus = false;
            }
        }

//----------------------------- Button open file with urls ----------------------------------------------//

        Button {
            id: btn_urls
            height: url_field.height
            width: height
            anchors.left: url_field.right
            anchors.verticalCenter: url_field.verticalCenter
            anchors.leftMargin: 15
            icon.source: 'openurls.png'
            icon.color: 'transparent'
            icon.width: width * 0.9
            icon.height: icon.width
            background: Rectangle { color: btn_urls.pressed ? color_press : btn_urls.hovered ? color_hover : 'white'; }

            onReleased: {
                urls_file_dialog.open();
            }
        }

        FileDialog {
            id: urls_file_dialog
            title: 'Choose file with urls'

            onAccepted: {
                url_field.text = file;
            }
        }

//----------------------------- Label count of chapters ----------------------------------------------//

        Text {
            id: chapter_count_text
            text: 'Count of chapters\n' + '* for all available'
            font.family: 'Arial'
            font.pixelSize: 16
            anchors.left: chapter_url_text.left
            anchors.top: url_field.bottom
            anchors.topMargin: 40
        }

//----------------------------- Field with count of chapters ----------------------------------------------//

        TextField {
            id: chapter_count_field
            anchors.left: chapter_url_text.left
            width: 70
            horizontalAlignment: Text.AlignHCenter

            validator: RegExpValidator { regExp: /[0-9*]+/ }

            anchors.top: chapter_count_text.bottom
            anchors.topMargin: 10
            height: 50

            background: Rectangle { radius: 10; border.width: 1; color: chapter_count_field.focus ?
                    color_press : chapter_count_field.hovered ? color_hover : 'white'; }

            placeholderText: "1"
            font.pixelSize: 18

            onAccepted: {
                focus = false;
            }

            onEditingFinished: {
                focus = false;
            }
        }

        CheckBox {
            id: try_download_next_chapter
            visible: false
            text: 'Try download next chapter'
            font.pixelSize: 16
            font.family: 'Arial'
            anchors.left: chapter_count_field.right
            anchors.verticalCenter: chapter_count_field.verticalCenter
            anchors.leftMargin: 100
        }

//----------------------------- Button save folder ----------------------------------------------//

        Button {
            id: chooseSaveFolder
            height: chapter_count_field.height
            width: height

            icon.source: 'savefolder.png'
            icon.color: 'transparent'
            icon.width: width * 0.9
            icon.height: icon.width

            anchors.verticalCenter: chapter_count_field.verticalCenter
            anchors.left: btn_urls.left

            background: Rectangle { color: chooseSaveFolder.pressed ?
                 color_press : chooseSaveFolder.hovered ? color_hover : 'white'; }

            onReleased: {
                chooseSaveFolderDialog.open();
            }
        }

        FolderDialog {
            title: "Choose save folder"
            id: chooseSaveFolderDialog
        }
    }

//----------------------------- Button PARSE ----------------------------------------------//

    Button {
        id: startParse
        width: 150
        height: 50
        text: "Parse"
        font.pixelSize: height / 2
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.margins: 50

        background: Rectangle { radius: 5; border.width: 1; color: startParse.pressed ?
             color_press : startParse.hovered ? color_hover : 'white'; }

        onReleased: {
            parser.parse(url_field.text, slider_timeout.value, chooseSaveFolderDialog.folder,
            redownload_images_field.text, do_archive.checked, chapter_count_field.text);
        }
    }
}
