# Makefile - Pipeline Automatizado CO-RA
# Generación de videos y gestión de eventos de streaming

.PHONY: video event deploy clean help

# Variables por defecto
SUJETO ?= sueldos_morelos
DATOS ?= content/$(SUJETO)/data/datos.csv
GUION ?= content/$(SUJETO)/scripts/guion.md
BROLL ?= content/$(SUJETO)/broll/clip1.mp4
MUSIC ?= content/$(SUJETO)/music/track.mp3

# Comando principal: generar video completo
video:
	@echo "🚀 Generando video: $(SUJETO)"
	@echo "📊 Datos: $(DATOS)"
	@echo "📝 Guion: $(GUION)"
	
	# Verificar archivos requeridos
	@test -f $(DATOS) || (echo "❌ Error: $(DATOS) no encontrado" && exit 1)
	@test -f $(GUION) || (echo "❌ Error: $(GUION) no encontrado" && exit 1)
	
	# Generar gráficos
	@echo "📊 Generando gráficos..."
	python3 scripts/build_charts.py $(DATOS) content/$(SUJETO)/out
	
	# Generar subtítulos
	@echo "📝 Generando subtítulos..."
	python3 scripts/md_to_srt.py $(GUION) content/$(SUJETO)/out/subs.srt
	
	# Renderizar video
	@echo "🎬 Renderizando video..."
	bash scripts/render_video.sh $(SUJETO) $(BROLL) $(MUSIC)
	
	# Generar assets de publicación
	@echo "📱 Generando assets de publicación..."
	$(MAKE) publish-assets SUJETO=$(SUJETO)
	
	@echo "✅ Video completado: content/$(SUJETO)/out/video_final.mp4"

# Generar assets para publicación
publish-assets:
	@echo "📱 Generando título y descripción..."
	@echo "# $(shell echo $(SUJETO) | tr '_' ' ' | sed 's/.*/\L&/; s/[a-z]*/\u&/g')" > content/$(SUJETO)/out/titulo.txt
	@echo "¿Por qué hay tanta diferencia? 📊 Análisis completo de datos oficiales." >> content/$(SUJETO)/out/titulo.txt
	
	@echo "📋 Generando descripción..."
	@echo "🔍 Análisis detallado de $(shell echo $(SUJETO) | tr '_' ' ')" > content/$(SUJETO)/out/descripcion.txt
	@echo "📊 Datos oficiales y verificados" >> content/$(SUJETO)/out/descripcion.txt
	@echo "💡 Insights y conclusiones clave" >> content/$(SUJETO)/out/descripcion.txt
	@echo "" >> content/$(SUJETO)/out/descripcion.txt
	@echo "🔗 Más análisis en: tu-sitio.com" >> content/$(SUJETO)/out/descripcion.txt
	@echo "" >> content/$(SUJETO)/out/descripcion.txt
	@echo "#$(shell echo $(SUJETO) | tr '_' ' ' | sed 's/ //g') #Datos #Análisis #Transparencia" >> content/$(SUJETO)/out/descripcion.txt

# Crear evento de streaming
event:
	@echo "🎪 Creando evento de streaming..."
	@test -n "$(EVENT)" || (echo "❌ Error: Especifica EVENT=nombre_evento" && exit 1)
	bash tenancingo_live/scripts/create_event.sh $(EVENT)

# Desplegar infraestructura
deploy:
	@echo "🚀 Desplegando infraestructura..."
	cd tenancingo_live && docker-compose up -d
	@echo "✅ Servicios desplegados:"
	@echo "   📺 RTMP: rtmp://localhost:1935/live"
	@echo "   🌐 Web: http://localhost:8080"
	@echo "   📡 HLS: http://localhost:8081/hls/"

# Detener servicios
stop:
	@echo "🛑 Deteniendo servicios..."
	cd tenancingo_live && docker-compose down

# Limpiar archivos temporales
clean:
	@echo "🧹 Limpiando archivos temporales..."
	find content -name "*.tmp" -delete
	find content -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Limpieza completada"

# Configurar proyecto nuevo
setup:
	@echo "⚙️  Configurando proyecto..."
	@test -n "$(PROYECTO)" || (echo "❌ Error: Especifica PROYECTO=nombre" && exit 1)
	
	# Crear estructura
	mkdir -p content/$(PROYECTO)/{data,broll,music,out,scripts}
	
	# Crear archivos de ejemplo
	@echo "# Guion para $(PROYECTO)" > content/$(PROYECTO)/scripts/guion.md
	@echo "" >> content/$(PROYECTO)/scripts/guion.md
	@echo "Introducción al tema de $(PROYECTO)." >> content/$(PROYECTO)/scripts/guion.md
	@echo "Datos principales y hallazgos." >> content/$(PROYECTO)/scripts/guion.md
	@echo "Conclusiones y llamada a la acción." >> content/$(PROYECTO)/scripts/guion.md
	
	@echo "puesto,salario" > content/$(PROYECTO)/data/datos.csv
	@echo "Ejemplo 1,25000" >> content/$(PROYECTO)/data/datos.csv
	@echo "Ejemplo 2,35000" >> content/$(PROYECTO)/data/datos.csv
	@echo "Ejemplo 3,45000" >> content/$(PROYECTO)/data/datos.csv
	
	@echo "✅ Proyecto $(PROYECTO) configurado en content/$(PROYECTO)/"
	@echo "📝 Edita: content/$(PROYECTO)/scripts/guion.md"
	@echo "📊 Edita: content/$(PROYECTO)/data/datos.csv"
	@echo "🎵 Añade: content/$(PROYECTO)/music/track.mp3"
	@echo "🎬 Añade: content/$(PROYECTO)/broll/clip1.mp4"

# Verificar dependencias
check:
	@echo "🔍 Verificando dependencias..."
	@command -v python3 >/dev/null 2>&1 || (echo "❌ Python3 no encontrado" && exit 1)
	@command -v ffmpeg >/dev/null 2>&1 || (echo "❌ FFmpeg no encontrado" && exit 1)
	@command -v docker >/dev/null 2>&1 || (echo "❌ Docker no encontrado" && exit 1)
	@python3 -c "import pandas, matplotlib" 2>/dev/null || (echo "❌ Librerías Python faltantes: pip install pandas matplotlib" && exit 1)
	@echo "✅ Todas las dependencias están instaladas"

# Ayuda
help:
	@echo "🎬 Pipeline Automatizado CO-RA"
	@echo "================================"
	@echo ""
	@echo "📊 GENERACIÓN DE VIDEOS:"
	@echo "  make video SUJETO=nombre DATOS=archivo.csv GUION=guion.md"
	@echo "  make setup PROYECTO=nuevo_proyecto"
	@echo ""
	@echo "🎪 STREAMING:"
	@echo "  make event EVENT=nombre_evento"
	@echo "  make deploy"
	@echo "  make stop"
	@echo ""
	@echo "🔧 UTILIDADES:"
	@echo "  make check    - Verificar dependencias"
	@echo "  make clean    - Limpiar archivos temporales"
	@echo "  make help     - Mostrar esta ayuda"
	@echo ""
	@echo "📁 ESTRUCTURA:"
	@echo "  content/SUJETO/data/     - CSV con datos"
	@echo "  content/SUJETO/scripts/  - Guion en Markdown"
	@echo "  content/SUJETO/broll/    - Video de fondo"
	@echo "  content/SUJETO/music/    - Música de fondo"
	@echo "  content/SUJETO/out/      - Archivos generados"