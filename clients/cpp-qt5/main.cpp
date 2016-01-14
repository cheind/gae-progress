
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
    parser.addPositionalArgument("command", "Which command to execute. Choose from create,list.");
    
    // Common arguments accross all tasks
    QCommandLineOption url("url", "URL of app server", "URL", "http://localhost:8080");
    QCommandLineOption apikey("key", "API-key to access resource", "String");
    
    // Create specific arguments
    QCommandLineOption title("title", "Title of progress to create", "String");
    QCommandLineOption desc("desc", "Description of progress to create", "String");
    QCommandLineOption prog("progress", "Progress value", "Float", "0.0");
    
    
    parser.addOption(url);
    parser.addOption(apikey);
    parser.addOption(title);
    parser.addOption(desc);
    parser.addOption(prog);
    
    
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
    } else if (command == "create") {
        ProgressCreateTask *t = new ProgressCreateTask(&app);
        t->setTitle(parser.value(title));
        t->setDescription(parser.value(desc));
        t->setProgress(parser.value(prog).toFloat());
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