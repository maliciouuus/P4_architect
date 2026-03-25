# Contexte du projet DataShare

## Besoin métier

DataShare souhaite un **prototype** de plateforme pour envoyer des fichiers de façon **simple et sécurisée**, avec des **liens de téléchargement** à durée limitée. Le public visé : freelances et petites structures.

## Périmètre MVP (rappel)

Fonctionnalités prévues pour la première version :

- création de compte et connexion ;
- envoi de fichier une fois connecté ;
- lien unique pour télécharger le fichier ;
- historique des envois pour l’utilisateur ;
- suppression manuelle d’un fichier ;
- règles métier : taille max, durée de validité du lien, éventuel mot de passe sur le fichier (selon avancement).

Les fonctionnalités « avancées » du cahier (upload anonyme, tags, etc.) restent **optionnelles** pour la démonstration MVP.

## Approche technique retenue

Le développement se fera avec une **API REST** (Django / Django REST Framework) et une interface **Vue.js**, une base **PostgreSQL** et un stockage fichier sur **disque local** pour le prototype.

## Suivi du travail

Les livrables demandés (documentation, tests, sécurité, performance, maintenance) seront ajoutés **progressivement** dans le dépôt, en lien avec le code.
