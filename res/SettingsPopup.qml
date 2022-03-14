import QtQuick 2.15
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.15

Popup {
    id: settings_popup

    property string config_save_folder: ''
    property string config_path_to_browser: ''

    property bool config_auto_update: false
    property bool config_remember_save_folder: true
    property bool config_notifications: true

    property int config_requests_limit: 100
    property int config_semaphore_limit: 200
    property int config_download_tries: 5

    modal: true

    background: Rectangle { border.color: "black"; radius: 20; color: color_base; }

    enter: Transition {
        NumberAnimation { property: 'opacity'; from: 0; to: 1; duration: 200 }
    }

    exit: Transition {
        NumberAnimation { property: 'opacity'; from: 1; to: 0; duration: 200 }
    }

    onClosed: { update_config_file_vars(); }

    ToolBar {
        id: tool_bar
        background: Rectangle {color: 'transparent'}

        anchors.top: parent.top
        anchors.left: parent.left
        anchors.margins: 20

        Row {
            spacing: 20

            Button {
                id: base_settings
                height: 30
                width: 150
                font.pixelSize: 17
                font.family: 'Arial'
                focus: true

                text: 'Main'

                background: Rectangle { radius: 10; border.width: 1; color: base_settings.focus ?
                        color_press : base_settings.hovered ? color_hover : 'white'; }
                onReleased: { loader.sourceComponent = main_settings_rect; }
            }

            Button {
                id: browser_driver_settings
                height: 30
                width: 150
                font.pixelSize: 17
                font.family: 'Arial'

                text: 'Browser'

                onReleased: { loader.sourceComponent = browser_settings_rect; }

                background: Rectangle { radius: 10; border.width: 1; color: browser_driver_settings.focus ?
                        color_press : browser_driver_settings.hovered ? color_hover : 'white'; }
            }

            Button {
                id: download_settings
                height: 30
                width: 150
                font.pixelSize: 17
                font.family: 'Arial'

                text: 'Download'

                onReleased: { loader.sourceComponent = download_settings_rect; }

                background: Rectangle { radius: 10; border.width: 1; color: download_settings.focus ?
                        color_press : download_settings.hovered ? color_hover : 'white'; }
            }

            Button {
                id: about_settings
                height: 30
                width: 150
                font.pixelSize: 17
                font.family: 'Arial'

                text: 'About'

                onReleased: { loader.sourceComponent = about_settings_rect; }

                background: Rectangle { radius: 10; border.width: 1; color: about_settings.focus ?
                        color_press : about_settings.hovered ? color_hover : 'white'; }
            }
        }
    }

    Rectangle {
        visible: false
        height: 1
        width: parent.width * 0.95
        anchors.top: tool_bar.bottom
        anchors.margins: 10
        anchors.horizontalCenter: parent.horizontalCenter
        color: 'black'
    }


    Loader {
        id: loader
        anchors.top: tool_bar.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 20
        anchors.topMargin: 30

        sourceComponent: main_settings_rect
    }
// ------------------------------------------ Main Settings Component ------------------------//
    Component {
        id: main_settings_rect
        Rectangle {
            border.width: 1
            radius: 20

            Text {
                text: 'Main settings'
                font.family: 'Arial'
                font.pixelSize: 18
                font.italic: true
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 15
            }

            Column {
                property int cur_height: 25
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.margins: 30
                anchors.top: parent.top
                anchors.topMargin: 60

                Row {
                    height: parent.cur_height
                    width: parent.width

                    Text {
                        text: 'Remember the last save folder'
                        font.pixelSize: 19
                        font.family: 'Arial'
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    Switch {
                        padding: 0
                        topInset: 0
                        bottomInset: 0
                        checked: config_remember_save_folder
                        anchors.right: parent.right
                        anchors.verticalCenter: parent.verticalCenter
                        onReleased: { config_remember_save_folder = checked; }
                    }
                }

                Row { height: parent.cur_height; width: parent.width;
                    Rectangle { color: 'grey'; height: 1; width: parent.width; anchors.verticalCenter: parent.verticalCenter; }}

                Row {
                    height: parent.cur_height
                    width: parent.width

                    Text {
                        text: 'Current save folder'
                        font.pixelSize: 19
                        font.family: 'Arial'
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    Text {
                        font.family: 'Arial'
                        font.pixelSize: 14
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.right: parent.right
                        text: config_save_folder == '' ? 'Root' : config_save_folder
                    }
                }

//                Row { height: parent.cur_height; width: parent.width;
//                    Rectangle { color: 'grey'; height: 1; width: parent.width; anchors.verticalCenter: parent.verticalCenter; }}

//                Row {
//                    height: parent.cur_height
//                    width: parent.width

//                    Text {
//                        text: 'Auto update'
//                        font.pixelSize: 19
//                        font.family: 'Arial'
//                        anchors.verticalCenter: parent.verticalCenter
//                    }

//                    Switch {
//                        id: autoupdate
//                        padding: 0
//                        topInset: 0
//                        bottomInset: 0
//                        checked: config_auto_update
//                        anchors.right: parent.right
//                        anchors.verticalCenter: parent.verticalCenter
//                        onReleased: { config_auto_update = checked; }
//                    }
//                }

//                Row { height: parent.cur_height; width: parent.width;
//                    Rectangle { color: 'grey'; height: 1; width: parent.width; anchors.verticalCenter: parent.verticalCenter; }}

//                Row {
//                    height: parent.cur_height
//                    width: parent.width

//                    Text {
//                        text: 'Available updates'
//                        font.pixelSize: 19
//                        font.family: 'Arial'
//                        anchors.verticalCenter: parent.verticalCenter
//                    }

//                    Button {
//                        enabled: text == 'No' ? false : true
//                        height: parent.cur_height
//                        anchors.verticalCenter: parent.verticalCenter
//                        anchors.right: parent.right

//                        background: Rectangle { color: 'transparent' }

//                        font.family: 'Arial'
//                        font.pixelSize: 19
//                        text: 'No'
//                        padding: 0
//                        leftInset: 0

//                        palette.buttonText: pressed ? '#005c84' : hovered ? '#0082B9' : 'black'
//                    }
//                }

                Row { height: parent.cur_height; width: parent.width;
                    Rectangle { color: 'grey'; height: 1; width: parent.width; anchors.verticalCenter: parent.verticalCenter; }}

                Row {
                    height: parent.cur_height
                    width: parent.width

                    Text {
                        text: 'Notifications'
                        font.pixelSize: 19
                        font.family: 'Arial'
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    Switch {
                        padding: 0
                        topInset: 0
                        bottomInset: 0
                        checked: config_notifications
                        anchors.right: parent.right
                        anchors.verticalCenter: parent.verticalCenter
                        onReleased: { config_notifications = checked; }
                    }
                }

                Row { height: parent.cur_height; width: parent.width;
                    Rectangle { color: 'grey'; height: 1; width: parent.width; anchors.verticalCenter: parent.verticalCenter; }}

                Row {
                    height: parent.cur_height
                    width: parent.width

                    Button {
                        anchors.verticalCenter: parent.verticalCenter
                        height: parent.cur_height
                        background: Rectangle { color: 'transparent' }

                        font.family: 'Arial'
                        font.pixelSize: 19
                        text: 'Show last saved log'
                        padding: 0
                        leftInset: 0

                        palette.buttonText: pressed ? '#005c84' : hovered ? '#0082B9' : 'black'

                        onReleased: { parser.show_log(); }
                    }
                }

                Row { height: parent.cur_height; width: parent.width;
                    Rectangle { color: 'grey'; height: 1; width: parent.width; anchors.verticalCenter: parent.verticalCenter; }}

                Row {
                    height: parent.cur_height
                    width: parent.width

                    Button {
                        anchors.verticalCenter: parent.verticalCenter
                        height: parent.cur_height
                        background: Rectangle { color: 'transparent' }

                        font.family: 'Arial'
                        font.pixelSize: 19
                        text: 'Get the help!   HEEEEEEEEEEEEEEELP!!!'
                        padding: 0
                        leftInset: 0

                        palette.buttonText: pressed ? '#005c84' : hovered ? '#0082B9' : 'black'

                        onReleased: { parser.get_the_help(); }
                    }
                }
            }
        }
    }
// ------------------------------------------ Browser Settings Component ------------------------//
    Component {
        id: browser_settings_rect
        Rectangle {
            border.width: 1
            radius: 20

            Text {
                text: 'Browser & Driver settings'
                font.family: 'Arial'
                font.pixelSize: 18
                font.italic: true
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 15
            }

            Column {
                property int cur_height: 25
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.margins: 30
                anchors.top: parent.top
                anchors.topMargin: 60

// ------------------------------------------ Set up location of browser ------------------------//
                Row {
                    clip: true
                    width: parent.width
                    height: parent.cur_height

                    Button {
                        height: parent.cur_height
                        padding: 0
                        leftInset: 0
                        anchors.verticalCenter: parent.verticalCenter

                        background: Rectangle { color: 'transparent' }

                        font.family: 'Arial'
                        font.pixelSize: 19
                        text: 'Chrome / Chromium location'

                        palette.buttonText: pressed ? '#005c84' : hovered ? '#0082B9' : 'black'

                        onReleased: { browser_location_settings_popup.open(); }
                    }

                    Text {
                        font.family: 'Arial'
                        font.pixelSize: 14
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.right: parent.right
                        text: config_path_to_browser == '' ? '???' : config_path_to_browser
                    }
                }

                Row { height: parent.cur_height; width: parent.width;
                    Rectangle { color: 'grey'; height: 1; width: parent.width; anchors.verticalCenter: parent.verticalCenter; }}

// ------------------------------------------ Check Version of browser ------------------------//
                Row {
                    height: parent.cur_height
                    width: parent.width

                    Text {
                        text: 'Version of your Chrome | Chromium'
                        font.pixelSize: 19
                        font.family: 'Arial'
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    Text {
                        font.pixelSize: 19
                        font.family: 'Arial'
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.right: parent.right

                        Component.onCompleted: { text = parser.get_browser_version(); }
                    }
                }

                Row { height: parent.cur_height; width: parent.width;
                    Rectangle { color: 'grey'; height: 1; width: parent.width; anchors.verticalCenter: parent.verticalCenter; }}

// ------------------------------------------ Check Chromedriver ------------------------//
                Row {
                    height: parent.cur_height
                    width: parent.width
                    Text {
                        id: status
                        property string value: '  ???'
                        text: 'Status: ' + value
                        font.pixelSize: 19
                        font.family: 'Arial'
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.right: parent.right
                        color: value == '   Ok' ? 'green' : value == 'Error' ? 'red' : 'black'
                    }

                    Button {
                        height: parent.cur_height
                        anchors.verticalCenter: parent.verticalCenter

                        background: Rectangle { color: 'transparent' }

                        font.family: 'Arial'
                        font.pixelSize: 19
                        text: 'Check driver'
                        padding: 0
                        leftInset: 0

                        palette.buttonText: pressed ? '#005c84' : hovered ? '#0082B9' : 'black'

                        onReleased: {
                            var b = parser.check_driver();
                            if (b === 'True') status.value = '   Ok';
                            else status.value = 'Error';
                        }
                    }
                }
                Row { height: parent.cur_height; width: parent.width;
                    Rectangle { color: 'grey'; height: 1; width: parent.width; anchors.verticalCenter: parent.verticalCenter; }}

// ------------------------------------------ Download Chromedriver ------------------------//
                Row {
                    height: parent.cur_height
                    width: parent.width

                    Button {
                        anchors.verticalCenter: parent.verticalCenter
                        height: parent.cur_height
                        background: Rectangle { color: 'transparent' }

                        font.family: 'Arial'
                        font.pixelSize: 19
                        text: 'Download the correct driver'
                        padding: 0
                        leftInset: 0

                        palette.buttonText: pressed ? '#005c84' : hovered ? '#0082B9' : 'black'

                        onReleased: {
                            status.value = ' Wait';
                            parser.download_chromedriver();
                            var b = parser.check_driver();
                            if (b === 'True') status.value = '   Ok';
                            else status.value = 'Error';
                        }
                    }
                }
            }
        }
    }
// ------------------------------------------ Download settings Component ------------------------//
    Component {
        id: download_settings_rect
        Rectangle {
            border.width: 1
            radius: 20

            Text {
                text: 'Download settings'
                font.family: 'Arial'
                font.pixelSize: 18
                font.italic: true
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 15
            }

            Column {
                property int cur_height: 25
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.margins: 30
                anchors.top: parent.top
                anchors.topMargin: 60

// ------------------------------------------ Limit for asyncio download ------------------------//
                Row {
                    height: parent.cur_height
                    width: parent.width
                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        text: 'Base limits to requests'
                        font.pixelSize: 19
                        font.family: 'Arial'
                    }

                    TextField {
                        id: limits_value
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.right: parent.right
                        font.pixelSize: 19
                        background: Rectangle {color: 'transparent'}
                        text: config_requests_limit
                        selectionColor: 'white'
                        validator: RegularExpressionValidator {regularExpression: /[0-9]+/}
                        onAccepted: { focus = false; config_requests_limit = Number(text); }
                    }
                }

                Row { height: parent.cur_height; width: parent.width;
                    Rectangle { color: 'grey'; height: 1; width: parent.width; anchors.verticalCenter: parent.verticalCenter; }}

// ------------------------------------------ Semaphore for asyncio ------------------------//
                Row {
                    height: parent.cur_height
                    width: parent.width

                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        text: 'Base semaphore value'
                        font.pixelSize: 19
                        font.family: 'Arial'
                    }

                    TextField {
                        id: semaphore_value
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.right: parent.right
                        font.pixelSize: 19
                        validator: RegularExpressionValidator {regularExpression: /[0-9]+/}
                        background: Rectangle {color: 'transparent'}
                        text: config_semaphore_limit
                        selectionColor: 'white'
                        onAccepted: { focus = false; config_semaphore_limit = Number(text); }
                    }
                }
                
                Row { height: parent.cur_height; width: parent.width;
                    Rectangle { color: 'grey'; height: 1; width: parent.width; anchors.verticalCenter: parent.verticalCenter; }}

// ------------------------------------------ Download retries ------------------------//
                Row {
                    height: parent.cur_height
                    width: parent.width

                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        text: 'Count of tries to download'
                        font.pixelSize: 19
                        font.family: 'Arial'
                    }

                    TextField {
                        id: retries_value
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.right: parent.right
                        font.pixelSize: 19
                        validator: RegularExpressionValidator {regularExpression: /[0-9]+/}
                        background: Rectangle {color: 'transparent'}
                        text: config_download_tries
                        selectionColor: 'white'
                        onAccepted: { focus = false; config_download_tries = Number(text); }
                    }
                }
            }
        }
    }
// ------------------------------------------ About Component ------------------------//
    Component {
        id: about_settings_rect
        Rectangle {
            border.width: 1
            radius: 20

            Text {
                text: 'About & Contact'
                font.family: 'Arial'
                font.pixelSize: 18
                font.italic: true
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 15
            }

            Column {
                anchors.fill: parent
                anchors.margins: 100
                anchors.leftMargin: 200
                spacing: 25

                FontLoader { id: wildwords; source: 'font.ttf'; }

                Row {
                    width: parent.width
                    height: 64
                    spacing: 25

                    Image {
                        mipmap: true
                        source: 'icon.png'
                        height: 64
                        width: height
                        fillMode: Image.PreserveAspectFit
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    Text {
                        text: 'WebParser v1.5'
                        font.pixelSize: 40
                        font.family: wildwords.name
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }

                Row {
                    width: parent.width
                    height: 32
                    spacing: 25
                    anchors.left: parent.left
                    anchors.leftMargin: 32

                    Image {
                        mipmap: true
                        source: 'tools.png'
                        height: 32
                        width: height
                        fillMode: Image.PreserveAspectFit
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    Text {
                        text: 'Python + pyQt5 + QML'
                        font.pixelSize: 18
                        font.family: wildwords.name
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }

                Row {
                    width: parent.width
                    height: 32
                    spacing: 25
                    anchors.left: parent.left
                    anchors.leftMargin: 32

                    Image {
                        mipmap: true
                        source: 'trello.png'
                        height: 32
                        width: height
                        fillMode: Image.PreserveAspectFit
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    Text {
                        text: '<html><a href="https://trello.com/b/YaGVlIR5/webparser">Visit me on Trello</a></html>'
                        font.pixelSize: 18
                        font.family: wildwords.name
                        anchors.verticalCenter: parent.verticalCenter
                        onLinkActivated: Qt.openUrlExternally(link)
                    }
                }

                Row {
                    width: parent.width
                    height: 32
                    spacing: 25
                    anchors.left: parent.left
                    anchors.leftMargin: 32

                    Image {
                        mipmap: true
                        source: 'github.png'
                        height: 32
                        width: height
                        fillMode: Image.PreserveAspectFit
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    Text {
                        text: '<html><a href="https://github.com/skilletfun/webparser_release">Visit me on GitHub</a></html>'
                        font.pixelSize: 18
                        font.family: wildwords.name
                        anchors.verticalCenter: parent.verticalCenter
                        onLinkActivated: Qt.openUrlExternally(link)
                    }
                }

                Row {
                    width: parent.width
                    height: 32
                    spacing: 25
                    anchors.left: parent.left
                    anchors.leftMargin: 32

                    Image {
                        mipmap: true
                        source: 'discord.png'
                        height: 32
                        width: height
                        fillMode: Image.PreserveAspectFit
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    Text {
                        text: 'skilletfun#1388'
                        font.pixelSize: 18
                        font.family: wildwords.name
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }
            }
        }
    }

//------------------------------------- Popup Browser Location Settings ---------------------------//

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

            text: 'Path to Google Chrome | Chromium Data'
            font.family: 'Arial'
            font.pixelSize: 16

            x: 45
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.margins: 15
        }

        TextField {
            id: browser_location_field

            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: browser_location_text.bottom
            anchors.margins: 15
            anchors.topMargin: 10

            placeholderText: config_path_to_browser

            height: 50

            selectionColor: 'white'

            background: Rectangle { radius: 10; border.width: 1; color: browser_location_field.focus ?
                    color_press : browser_location_field.hovered ? color_hover : 'white'; }

            font.pixelSize: 18

            onAccepted: {
                focus = false;
                config_path_to_browser = text;
            }

            onEditingFinished: { focus = false; }
        }
    }

    Component.onCompleted: { update_config_qml_vars(); }

    function update_config_qml_vars()
    {
        var json = JSON.parse(String(parser.get_current_config()));

        config_save_folder = json.save_folder;
        config_path_to_browser = json.path_to_browser;

        config_auto_update = json.auto_update;
        config_remember_save_folder = json.remember_save_folder;
        config_notifications = json.notifications;

        config_requests_limit = json.request_limit;
        config_semaphore_limit = json.semaphore_limit;
        config_download_tries = json.download_tries;
        
        config_auto_update = json.auto_update;
    }

    function update_config_file_vars()
    {
        var config = {
            save_folder: config_save_folder,
            path_to_browser: config_path_to_browser,

            auto_update: config_auto_update,
            remember_save_folder: config_remember_save_folder,
            notifications: config_notifications,

            requests_limit: config_requests_limit,
            semaphore_limit: config_semaphore_limit,
            auto_update: config_auto_update,
            download_tries: config_download_tries
        };

        var str_config = JSON.stringify(config);
        parser.update_config_file(str_config);
    }
}
