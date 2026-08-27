<script>
(() => {
  "use strict";

  const messages = {
    cPlayer: {
      defaultTitle: "Programme C",
      localOnly: "Local uniquement",
      stdin: "stdin",
      stdinHelp: "Entree standard du programme : saisir ici les valeurs que le programme lirait au clavier. Separer les valeurs par des espaces ou des retours a la ligne, par exemple : 12 14",
      outputs: "Sorties (stdout)",
      run: "Build & Run",
      reset: "Reset",
      starterCode: "Starter code",
      initializing: "Initialisation du runtime...",
      localOnlyOutput: "Exercice multi-fichiers : execution navigateur indisponible.\nTelecharger le starter code ou cloner le depot, puis utiliser les commandes locales indiquees sous l'exercice.\n",
      localOnlyStatus: "Exercice local uniquement.",
      compiling: "Compilation en cours...",
completed: [
    "Exécution terminée.",
    "Programme terminé. Aucun ordinateur n'a été blessé.",
    "Exécution terminée. Le processeur peut se reposer.",
    "Programme terminé. Il a survécu.",
    "Exécution terminée. C'était presque professionnel.",
    "Fin de l'exécution. Rien n'a pris feu.",
    "Programme terminé avec succès. Le compilateur semble satisfait.",
    "Exécution terminée. Vous pouvez maintenant prétendre que c'était prévu.",
    "Fin du programme. Aucun undefined behavior visible à l'œil nu.",
    "Exécution terminée. Mission accomplie, au moins pour cette fois."
],

completedWithErrors: [
    "Exécution terminée avec des erreurs. Consulter stderr.",
    "Le programme a terminé. stderr souhaite cependant vous parler.",
    "Exécution terminée avec quelques protestations du compilateur.",
    "Le programme s'est arrêté. stderr contient la version longue de l'histoire.",
    "Fin de l'exécution. Tout ne s'est pas passé exactement comme prévu.",
    "Exécution terminée avec erreurs. Le débogage peut commencer.",
    "Le programme a fait de son mieux. Consultez stderr pour les détails.",
    "Fin de l'exécution. stderr a visiblement quelque chose à ajouter.",
    "Exécution terminée avec erreurs. Une nouvelle occasion d'apprendre.",
    "Le programme s'est terminé. La dignité du code, un peu moins."
],
      runtimeError: "Erreur runtime: {error}\n",
      runtimeErrorStatus: "Erreur runtime.",
      referenceCompilation: "Compilation de reference du support.\n",
      runtimeUnavailableReference: "Runtime navigateur non installe : sortie de reference affichee sans compilation reelle.\n",
      runtimeUnavailableChanged: "Runtime navigateur non installe : impossible de compiler les modifications dans le navigateur.\nUtiliser les commandes locales indiquees sous l'exercice.\n",
      runtimeUnavailableStatus: "Runtime C navigateur absent : sortie de reference uniquement.",
      localMakefileStatus: "Exercice multi-fichiers : utiliser le Makefile local.",
      runtimeWaiting: "Runtime C navigateur detecte, mais pas encore pret.",
      runtimeReady: "Runtime C navigateur pret.",
    },
    embeddedExercise: {
      demoLabel: "Démonstration",
      interactiveLabel: "Exercice",
      browserRunnable: "En ligne",
      localOnly: "Sur votre machine",
      localVersion: "Version locale :",
      then: "puis",
    },
    contentType: {
      quiz: "Quiz",
      exercise: "Exercice",
      guidedReading: "Lecture guidée",
      example: "Exemple exécutable",
    },
    typing: {
      defaultTitle: "Lecture guidée",
      invalidAnnotation: "Annotation de lecture invalide : {error}",
      speed: "Vitesse",
      speedSlow: "Lente",
      speedNormal: "Normale",
      speedFast: "Rapide",
      soundMuted: "Son coupe",
      soundActive: "Son actif",
      reset: "Reinitialiser",
      showCComments: "Afficher les commentaires C",
      showGuidedReading: "Afficher la lecture guidee",
      cCommentsTitle: "Commentaires C",
      cCommentsBody: "Le code complet et ses commentaires C sont affiches.",
      ready: "",
      canvasLabel: "Code C anime",
      codeCopied: "Code copié.",
      codeCopyFailed: "Impossible de copier le code.",
      annotationAria: "Afficher le commentaire : {title}",
      start: "Demarrer l'animation",
    initialStep: "{total} Étapes",
      preparedTitle: "Prêt pour la lecture",
      preparedBody: "",
      play: "Lecture",
      next: "Suivant",
      typing: [    "Je tape vite, non ?",    "Mon clavier commence à chauffer.",    "Je me concentre pour ne pas faire d'erreur de syntaxe.",    "Vous remarquerez cette maîtrise exceptionnelle du clavier.",    "Normalement, à cette vitesse, il faut un permis.",    "Je connais évidemment tout ce code par cœur.",    "Aucune autocomplétion. Tout est dans les doigts.",    "Ne clignez pas des yeux, vous risquez de rater une ligne.",    "Le compilateur commence déjà à avoir peur.",    "Cette démonstration de frappe est totalement authentique."],
      pause: "Pause",
      paused: "Lecture en pause.",
      continue: "Continuer",
      explanationFallback: "Poursuivre la lecture pour afficher la suite du programme.",
      explanationPause:  [
    "Oui, je commente mon code. Ça arrive.",
    "Un commentaire utile. Profitez-en, ils sont rares.",
    "Ici, j'explique ce que le code aurait dû expliquer tout seul.",
    "Ce commentaire est principalement destiné à mon futur moi.",
    "Six mois plus tard, ce commentaire sera probablement faux.",
    "Je mets un commentaire ici pour faire croire que tout était prévu.",
    "Ce commentaire évite normalement trois minutes de confusion.",
    "Oui, le commentaire est presque plus long que le code.",
    "À cet endroit, même le compilateur apprécierait une explication.",
    "Un bon commentaire répond à « pourquoi ? ». Celui-ci fait de son mieux."
],
      step: "Etape {current} / {total}",
      completeStep: "Termine - {total} etapes",
      completeTitle: "",
      completeBody: "Survolez les commentaires pour les revoir",
      replay: "Rejouer",
      completed: [
    "Voilà. Tout était écrit. Vous pouvez maintenant relire.",
    "Vous avez tout vu. Théoriquement, donc, vous avez tout compris.",
    "Fin des commentaires. Le bouton « relire » reste une option parfaitement valable.",
    "Si un détail vous a échappé, c'est probablement le moment de revenir en arrière.",
    "Tous les commentaires ont été affichés. Oui, même celui que vous n'avez pas lu.",
    "C'est terminé. Vous pouvez faire semblant d'avoir tout retenu, ou relire.",
    "Vous êtes arrivé jusqu'ici. Une seconde lecture pourrait transformer l'exploit en compréhension.",
    "Plus aucun commentaire à afficher. Il reste uniquement à les lire.",
    "Tout a été expliqué. Plusieurs fois, probablement. Une relecture ne fera pas de mal.",
    "Fin de la visite guidée. Pour les détails, le code est toujours juste devant vous."
],
      noOpenAnnotation: "Marqueur /** */ sans annotation ouverte.",
      emptyAnnotation: "L'annotation \"{title}\" ne couvre aucun code.",
      nestedAnnotation: "L'annotation \"{title}\" doit etre fermee par /** */ avant une nouvelle annotation.",
      unclosedAnnotation: "L'annotation \"{title}\" n'est pas fermee par /** */.",
      noOpenBashAnnotation: "Marqueur ## sans annotation ouverte.",
      emptyBashAnnotation: "L'annotation \"{title}\" ne couvre aucune commande.",
      nestedBashAnnotation: "L'annotation \"{title}\" doit etre fermee par ## avant une nouvelle annotation.",
      unclosedBashAnnotation: "L'annotation \"{title}\" n'est pas fermee par ##.",
    },
    quiz: {
      valid: "Valide",
      todo: "A faire",
      validate: "Valider",
      hints: [   
    "Besoin d'un petit coup de pouce ?",
    
],
      correct: [
    "Bonne réponse. Quiz validé.",
    "C'est correct. Comme quoi, lire le code peut servir.",
    "Bonne réponse. Le compilateur pédagogique approuve.",
    "Quiz validé. Vous pouvez faire semblant que c'était évident.",
    "Correct. Cette fois, l'intuition était bien configurée.",
    "Bonne réponse. Aucun warning pédagogique à signaler.",
    "Quiz validé. Le hasard nie toute implication.",
    "Correct. Vous pouvez conserver cette réponse en production.",
    "Bonne réponse. Une erreur de moins entre vous et la perfection académique.",
    "Quiz validé. Inutile de recommencer. Pour l'instant."
],
      incorrect: [
    "Il manque au moins une bonne réponse. Le quiz, lui, n'a rien oublié.",
    "Presque. Enfin… suffisamment loin pour recommencer.",
    "Le résultat suggère une stratégie audacieuse : relire les questions.",
    "Quelques réponses semblent avoir été choisies avec une confiance admirable.",
    "Le quiz demande une nouvelle tentative. Le hasard aussi, probablement.",
    "Il reste quelques détails à maîtriser. Comme les bonnes réponses.",
    "Résultat insuffisant. Votre compilateur intérieur a encore quelques warnings.",
    "Une nouvelle tentative est recommandée. Avec éventuellement un peu moins d'intuition.",
    "Il manque au moins une bonne réponse. Bonne nouvelle : les questions sont toujours les mêmes.",
    "Vous pouvez recommencer. Cette fois, certaines réponses pourraient même être correctes."
],
      restart: "On efface tout et on recommence.",
      questionValid: "",
    },
    ntfy: {
      title: "Chat SAE-C",
      configuring: "Configuration...",
      settingsAria: "Configurer le groupe ntfy",
      settingsTitle: "Configurer le groupe",
      settingsButton: "Groupe",
      groupTitle: "Groupe ntfy",
      groupLabel: "Groupe de l'etudiant",
      visitor: "visiteur",
      cancel: "Annuler",
      save: "Enregistrer",
      messageCode: "Message C",
      liveQuestion: "Question live",
      visitorStatus: "Visiteur",
      sseUnavailable: "SSE indisponible",
      groupRequired: "Groupe requis",
      connected: "{group} connecte",
      reconnecting: "{group} reconnexion...",
    },
    theme: {
      light: "Mode clair",
      dark: "Mode sombre",
    },
    exerciseProgress: {
      count: "{completed}/{total} realise{plural}",
      plural: "s",
    },
  };

  function lookup(key) {
    return key.split(".").reduce((value, part) => value && value[part], messages);
  }

  function t(key, values = {}) {
    const value = lookup(key);
    const message = Array.isArray(value)
      ? value[Math.floor(Math.random() * value.length)]
      : value;
    if (typeof message !== "string") {
      return `[${key}]`;
    }
    return message.replace(/\{([A-Za-z0-9_]+)\}/g, (_match, name) => String(values[name] ?? `{${name}}`));
  }

  function apply(root = document) {
    root.querySelectorAll("[data-message]").forEach((element) => {
      element.textContent = t(element.dataset.message);
    });
  }

  window.SAECMessages = Object.freeze({ t, apply });
  if (typeof document !== "undefined") {
    apply(document);
  }
})();
</script>
