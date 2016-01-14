
#include <QtCore>
#include <QNetworkAccessManager>
#include <QCommandLineParser>

#include "tasks.h"

int main(int argc, char* argv[])
{
    QCoreApplication app(argc, argv);
    QCoreApplication::setApplicationName("progress");
    QCoreApplication::setApplicationVersion("1.0");
    
    QCommandLineParser parser;
    parser.setApplicationDescription("Interact with RESTful gae-progress API https://github.com/cheind/gae-progress");
    parser.addHelpOption();
    parser.addVersionOption();
    parser.addPositionalArgument("command", "Which command to execute. Choose from list,.");
    
    QCommandLineOption url("url", "URL of app server", "URL", "http://localhost:8080");
    QCommandLineOption apikey("key", "API-key to access resource", "String");
    
    parser.addOption(url);
    parser.addOption(apikey);
    
    parser.process(app);
    
    const QStringList args = parser.positionalArguments();
    if (args.empty()) {
        qDebug() << "No command given.";
        return -1;
    }
    
    QString command = args.at(0);
    
    QNetworkAccessManager mgr;
    
    ProgressTask *task = 0;
    
    if (command == "list") {
        ProgressListTask *t = new ProgressListTask(&app);
        task = t;
    } else {
        qDebug() << "Unknown command";
        return -1;
    }
    
    task->setNetworkAccessManager(&mgr);
    task->setAddress(parser.value(url));
    task->setApiKey(parser.value(apikey));
    
    QObject::connect(task, SIGNAL(taskCompleted()), &app, SLOT(quit()));
    QTimer::singleShot(0, task, SLOT(run()));
    
    app.exec();
    
    return 0;
}