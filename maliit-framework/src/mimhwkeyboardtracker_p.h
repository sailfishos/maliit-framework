/* * This file is part of Maliit framework *
 *
 * Copyright (C) 2011 Nokia Corporation and/or its subsidiary(-ies).
 * All rights reserved.
 *
 * Contact: maliit-discuss@lists.maliit.org
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License version 2.1 as published by the Free Software Foundation
 * and appearing in the file LICENSE.LGPL included in the packaging
 * of this file.
 */

// This file is based on mkeyboardstatetracker_p.h from libmeegotouch

#ifndef MIMHWKEYBOARDTRACKER_P_H
#define MIMHWKEYBOARDTRACKER_P_H

#include <QFile>
#include <QScopedPointer>
#include <QDBusPendingCallWatcher>

#include "mimsettings.h"

#ifdef HAVE_CONTEXTSUBSCRIBER
#include <contextproperty.h>
#endif

class MImHwKeyboardTracker;

class MImHwKeyboardTrackerPrivate
    : public QObject
{
    Q_OBJECT

public:
    explicit MImHwKeyboardTrackerPrivate(MImHwKeyboardTracker *q_ptr);
    ~MImHwKeyboardTrackerPrivate();

#ifdef HAVE_UDEV
    void detectEvdev();
    void tryEvdevDevice(const char *device);
    QFile *evdevFile;
    int evdevTabletModePending;
    bool evdevTabletMode;
#endif

#ifdef HAVE_MCE
    bool keyboardOpened;
#endif

#ifdef HAVE_CONTEXTSUBSCRIBER
    QScopedPointer<ContextProperty> keyboardOpenProperty;
#elif defined(Q_WS_MAEMO_5)
    MImSettings keyboardOpenConf;
#endif

    bool present;

public Q_SLOTS:
#ifdef HAVE_UDEV
    void evdevEvent();
#endif

#ifdef HAVE_MCE
    void mceKeyboardStateChanged(const QString &value);
    void handleMceKeyboardReply(QDBusPendingCallWatcher*);
#endif

Q_SIGNALS:
    void stateChanged();
};


#endif // MIMHWKEYBOARDTRACKER_P_H
