#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /tools/grafana/Install/Install-test-of-grafana-package
#   Description: Installation of grafana package and a check if grafana server runs
#   Author: Jan Kuřík <jkurik@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2021 Red Hat, Inc.
#
#   This program is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 2 of
#   the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see http://www.gnu.org/licenses/.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Include Beaker environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

PACKAGE="grafana"

rlJournalStart
    rlPhaseStartTest
        rlAssertRpm $PACKAGE || \
            { rlFail "$PACKAGE is not installed"; rlDie "Giving up"; }
        rlServiceStart grafana-server

        HTTP_CODE="000"
        RETRIES=12
        while [[ "${HTTP_CODE}" == "000" ]]; do
            rlRun -s "curl -X GET -s -w \"\\n%{http_code}\\n\" \
                http://localhost:3000/login" \
                0-255 "Checking if Grafana is alive and responding"
            HTTP_CODE=$(tail -n 1 ${rlRun_LOG})
            if [[ "${HTTP_CODE}" == "000" ]]; then
                ((RETRIES--))
                if [[ ${RETRIES} -eq 0 ]]; then
                    rlFail "Retry limit has been reached"
                    break
                fi
            else
                rlAssertEquals "Response code should be 200" "${HTTP_CODE}" "200"
                break
            fi
            rlRun "sleep 10" 0 "Give grafana more time to start"
        done
    rlPhaseEnd

    rlPhaseStartCleanup
        rlServiceRestore
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
