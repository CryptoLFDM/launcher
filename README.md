# Le launcher LFDM
## Ce petit soft en python regroupe plusieurs utilitaires.
Mais avant tout, un petit peu de lecture pour comprendre de quoi on parle.

### [![grafana](sample/logo/grafana.png)](https://grafana.com/oss/grafana/) c'est quoi ?



Grafana est un outil que nous mettons à disposition. Il va vous permettre de visualiser vos résultats d'une manière graphique. Les résultats y seront stocké plusieurs **heures/jours/mois**, cela reste à définir.

Les données sont stocké dans une sorte de base de données qui s'appelle elasticsearch.

### [![elasticsearch](sample/logo/elasticsearch.png)](https://www.elastic.co/fr/) c'est quoi ?


Elasticsearch est une sorte de base de données que nous utilisons pour stocker les métriques et données que grafana va lire.

### [![telegraf](sample/logo/telegraf.png)](https://www.influxdata.com/time-series-platform/telegraf/) c'est quoi ?


Telegraf est ce que l'on appelle un collecteur. Il permet de récolter des informations de métrologies ou des informations custom.
Nous l'utilisons pour récupérer les métriques systèmes / chia / T-rex. Tout est gérée via un template. 

## Le plot check

⚠️ Compatibles avec la version 1.2.2 => 1.2.9 de chia blockchain uniquement pour le moment. Chia ayant changé les patterns de logs sans pour autant le déclarer nous faisons au mieux

L'onglet plot check permet donc de lancer la commande plot check (vous n'avez qu'à chercher votre executable chia pour se faire). Vous aurez le résultat en local dans le launcher, mais aussi sur Le [grafana de l'équipe LFDM](https://grafana.ether-source.fr/d/oQbtWaInk/plot-check?orgId=6&refresh=30s) est donc à cette adresse. 

Pour lancer le plot check, vous avez besoin de faire deux choses :
 * Ajouter votre chemin du binaire chia. Il se trouve en general ici : ``C:\Users\%UserProfile%\AppData\Local\chia-blockchain\app-1.2.2\resources\app.asar.unpacked\daemon\chia.exe``. Ma version de chia est 1.2.2, il va falloir mettre la votre dans le path.
 * Mettre un Pseudo afin de retrouver vos résultats sur grafana.


![N|plot_chek_ui](./sample/ui/launcher_ui.PNG)


## La partie telegraf

La partie telegraf permet simplement de générer un template valide pour le collecteur telegraf, ainsi qu'une pre configuration pour pourvoir écrire dans les Elasticsearch LFDM.
Afin de le faire fonctionner, vous devez vous rapprocher de nous afin d'obtenir les identifiants nécessaires.

Une partie automatisée arriveras plus tard.

## La partie Farmer

Cette partie est en cours de development, mais l'idée est de pouvoir vous permettre de lancer un harvester chia depuis ici, sans pour autant avoir chia de lancé.

## Des examples de graphique que nous faisons

### Supervision pool 2miners
![N|2miner_1.png](./sample/ui/2miner_1.PNG)
![N|2miner_2.png](./sample/ui/2miner_2.PNG)
![N|2miner_3.png](./sample/ui/2miner_3.PNG)

### Supervision system

![N|system_stat.PNG](./sample/ui/system_stat.PNG)
![N|system_stat.PNG](./sample/ui/system_stat_2.PNG)
![N|watcher.PNG](./sample/ui/watcher_1.PNG)
![N|watcher.PNG](./sample/ui/watcher_2.PNG)
![N|watcher.PNG](./sample/ui/watcher_3.PNG)

### Plot check

![N|plot_check.PNG](./sample/ui/plot_check.PNG)

### Chia Monitoring

![N|chia_monitoring.PNG](./sample/ui/chia-pool_1.PNG)
![N|chia_monitoring.PNG](./sample/ui/chia_monitor.PNG)
