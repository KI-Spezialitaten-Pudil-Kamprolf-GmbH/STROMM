import datetime

class Verbraucher:
    def __init__(self, name, basis_verbrauch):
        # Ein Verbraucher, der Energie verbraucht.
        # Args:
        #   name (str): Der Name des Verbrauchers (z.B. "Stadt A", "Fabrik B").
        #   basis_verbrauch (float): Der Basisverbrauch des Verbrauchers (in MW).
        self.name = name
        self.basis_verbrauch = basis_verbrauch

    def verbrauch_anpassen_tageszeit(self):
        # Passt den Verbrauch basierend auf der Tageszeit an.
        # Dies ist eine sehr einfache Implementierung. Eine realistischere Simulation
        # würde komplexere Verbrauchsmuster verwenden.
        # Returns:
        #   float: Der angepasste Verbrauch (in MW).
        jetzt = datetime.datetime.now()
        stunde = jetzt.hour

        if 6 <= stunde < 18:  # Tagsüber höherer Verbrauch
            faktor = 1.2  # 20% höherer Verbrauch tagsüber
        elif 18 <= stunde < 22: #Abends noch höherer Verbrauch
            faktor = 1.5 #50% höherer Verbrauch am Abend
        else:  # Nachts niedriger Verbrauch
            faktor = 0.7  # 30% niedriger Verbrauch nachts

        return self.basis_verbrauch * faktor

    def verbrauchen(self):
        # Gibt den aktuellen Verbrauch zurück.
        return self.verbrauch_anpassen_tageszeit()

    def __str__(self):
        return f"{self.name}: {self.verbrauch_anpassen_tageszeit():.2f} MW"