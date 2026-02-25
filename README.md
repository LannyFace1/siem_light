# 🛡️ SIEM-Light  
### Secure Log Monitoring System (Docker-based Mini SIEM)

SIEM-Light ist ein containerisiertes Secure Log Monitoring System, 
das grundlegende Cybersecurity Detection-Mechanismen implementiert.

Dieses Projekt wurde als Lern- und Portfolioarbeit im Bereich:

- Cybersecurity
- Log Analysis
- Threat Detection
- Docker Security
- DevSecOps Grundlagen

entwickelt.

---

## 🎯 Projektziel

Ziel ist es, ein vereinfachtes Security Information and Event Management (SIEM) System zu entwickeln, das:

- Log-Dateien analysiert
- verdächtige Login-Versuche erkennt
- IP-Adressen auswertet
- Alerts generiert
- ein Web-Dashboard zur Visualisierung bereitstellt
- vollständig containerisiert läuft

Das Projekt soll reale Security-Grundlagen praktisch demonstrieren.

---

## 🚀 Quick Start

### 1. Clone and configuration

'''bash
git clone 
cd siem_ligght/
cp .env.example .env

## 🧱 Technologie-Stack

- Python 3
- Flask (Web Framework)
- SQLite (Event- & Alert-Speicherung)
- Docker
- docker-compose

Geplante Erweiterungen:

- Email Alerts
- Reverse Proxy (Nginx)
- GeoIP Analyse
- Integration mit Grafana
- Erweiterte Detection Rules

---

## 🏗️ Architektur (MVP)

Das System besteht aktuell aus einem einzelnen Docker-Container mit:

1. Log Parser  
2. Detection Engine  
3. SQLite Datenbank  
4. Web Dashboard  

Logs werden per Docker Volume eingebunden.

---

## 🔍 Kernfunktionen (MVP)

- Einlesen einer Log-Datei (z. B. auth.log)
- Erkennung von „Failed password“ Events
- Extraktion der IP-Adresse
- Zählen fehlgeschlagener Login-Versuche pro IP
- Alert-Erstellung bei:
  - mehr als 5 Fehlversuchen innerhalb von 5 Minuten

## 🔐 Security-Design

Dieses Projekt legt bewusst Wert auf Security Best Practices:

- Container läuft als **non-root User**
- Keine hardcodierten Secrets
- Konfiguration via ENV Variablen
- HEALTHCHECK im Dockerfile
- Minimal Base Image (python:slim)
- Unterstützung für read-only Filesystem
- Saubere Trennung von Parsing & Detection Logik

Ziel ist es, bereits im Lernprojekt sichere Standards zu etablieren.

---

## 📂 Projektstruktur
```
siem_light/
├──docker-compose.yml
├──.env.example
├──backend/
|   └──
|
|
├──forntend/
|   └──
```