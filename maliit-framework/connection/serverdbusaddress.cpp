/* * This file is part of Maliit framework *
 *
 * Copyright (c) 2010 Nokia Corporation and/or its subsidiary(-ies).
 * All rights reserved.
 * Copyright (c) 2021 Jolla Ltd.
 *
 * Contact: maliit-discuss@lists.maliit.org
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License version 2.1 as published by the Free Software Foundation
 * and appearing in the file LICENSE.LGPL included in the packaging
 * of this file.
 */

#include "serverdbusaddress.h"

#include <QDebug>
#include <QDBusConnection>

#include <QDBusServer>
#include <QDir>

#include <cstdlib>

#include <sys/stat.h>

#include <unistd.h>

namespace {
    const char * const MaliitServerName = "org.maliit.server";
    const char * const MaliitServerObjectPath = "/org/maliit/server/address";
}

namespace Maliit {
namespace Server {
namespace DBus {

AddressPublisher::AddressPublisher(const QString &address)
    : QObject()
    , mAddress(address)
{
    QDBusConnection::sessionBus().registerObject(MaliitServerObjectPath, this, QDBusConnection::ExportAllProperties);
    if (!QDBusConnection::sessionBus().registerService(MaliitServerName)) {
        qWarning("maliit-server is already running");
        std::exit(0);
    }
}

AddressPublisher::~AddressPublisher()
{
    QDBusConnection::sessionBus().unregisterObject(MaliitServerObjectPath);
}

QString AddressPublisher::address() const
{
    return mAddress;
}

Address::Address()
{}

Address::~Address()
{}

DynamicAddress::DynamicAddress()
{}

QDBusServer* DynamicAddress::connect()
{
    QDBusServer *server = nullptr;
    char *runDir = nullptr;
    char *socketDir = nullptr;
    char *socketFile = nullptr;
    const char *env = getenv("XDG_RUNTIME_DIR");
    if (env && *env == '/' && QDir(QString::fromUtf8(env)).exists())
        runDir = strdup(env);
    else if (asprintf(&runDir, "/run/user/%d", static_cast<int>(getuid())) < 0)
        runDir = nullptr;
    if (!runDir) {
        qWarning("Could not determine XDG_RUNTIME_DIR");
    } else if (asprintf(&socketDir, "%s/maliit-server", runDir) < 0) {
        socketDir = nullptr;
    } else if (asprintf(&socketFile, "%s/dbus-socket", socketDir) < 0) {
        socketFile = nullptr;
    } else if (mkdir(socketDir, 0770) == -1 && errno != EEXIST) {
        qWarning("Failed to create %s: %s", socketDir, strerror(errno));
    } else if (unlink(socketFile) == -1 && errno != ENOENT) {
        qWarning("Failed to remove %s: %s", socketFile, strerror(errno));
    } else {
        QString dbusAddress(QStringLiteral("unix:path=%1").arg(socketFile));
        server = new QDBusServer(dbusAddress);
        publisher.reset(new AddressPublisher(server->address()));
    }
    free(socketFile);
    free(socketDir);
    free(runDir);
    return server;
}

QDBusServer* FixedAddress::connect()
{
    QDBusServer *server = new QDBusServer(mAddress);

    return server;
}

FixedAddress::FixedAddress(const QString &address)
    : mAddress(address)
{}

} // namespace DBus
} // namespace Server
} // namespace Maliit
