
#include <QtCore>
#include <QUrl>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>
#include <QApplication>
#include <QDebug>

#include <QJsonDocument>
#include <QJsonObject>

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);

    QUrl url("http://localhost:8080/_ah/api/progressApi/v1/list");    
    QUrlQuery query;
    query.addQueryItem("apikey", "YOUR-API-KEY");    
    url.setQuery(query);

    QNetworkAccessManager mgr;
    QNetworkRequest req(url);
    QNetworkReply *reply = mgr.get(req);

    QObject::connect(reply, SIGNAL(finished()), &app, SLOT(quit()));

    app.exec();    
    
    if ((reply->error() == QNetworkReply::NoError)) {
       
        QJsonDocument doc = QJsonDocument::fromJson(reply->readAll());
        if (!doc.isNull() && doc.isObject()) {
            QJsonObject root = doc.object();
            QJsonArray items = root["items"].toArray();
            qDebug() << "Received" << items.size() << "items";
            qDebug() << "----------";
            for (int i = 0; i < items.size(); ++i) {
                QJsonObject item = items[i].toObject();
                qDebug() << "id:" << item["id"].toString();
                qDebug() << "created:" << item["created"].toString();
                qDebug() << "title:" << item["title"].toString();
                qDebug() << "progress:" << item["progress"].toInt();
                qDebug() << "----------";
            }
        }
    } else {
        qDebug() << "Error:" << reply->errorString();
    }

    return 0;
}