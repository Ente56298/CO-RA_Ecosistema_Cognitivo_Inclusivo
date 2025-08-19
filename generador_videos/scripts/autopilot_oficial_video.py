#!/usr/bin/env python3
"""
Generador Automático de Videos CO-RA
Sistema completo de 6 fases para crear videos con fuentes oficiales verificadas
"""

import os, re, json, base64, math, requests, pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip, afx
import tldextract
from datetime import datetime

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

OUTDIR = "./output"
os.makedirs(OUTDIR, exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0 (CO-RA Educational Bot)"}

# Dominios oficiales verificados
OFFICIAL_DOMAINS = [d.strip().lower() for d in os.getenv(
    "OFFICIAL_DOMAINS",
    ".gov,.edu,.who.int,.un.org,.worldbank.org,.gob.mx,.inegi.org.mx,.imf.org,.oecd.org"
).split(",")]

def is_official(url):
    """Verifica si una URL pertenece a un dominio oficial"""
    ext = tldextract.extract(url)
    dom = f"{ext.domain}.{ext.suffix}".lower()
    return any(dom.endswith(pat) for pat in OFFICIAL_DOMAINS)

def fetch_content(url):
    """Extrae contenido limpio de una URL oficial"""
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200: 
            return ""
        
        soup = BeautifulSoup(r.text, "html.parser")
        # Remover elementos no deseados
        for element in soup(["script", "style", "noscript", "nav", "footer", "header"]):
            element.decompose()
        
        return " ".join(soup.get_text(" ").split())
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def harvest_official_data(topic, limit=8):
    """FASE 0: Investigación en fuentes oficiales verificadas"""
    print(f"🔍 FASE 0: Investigando '{topic}' en fuentes oficiales...")
    
    # Semillas de sitios oficiales
    official_seeds = [
        "https://www.who.int",
        "https://www.un.org", 
        "https://www.worldbank.org",
        "https://www.imf.org",
        "https://www.oecd.org",
        "https://www.gob.mx",
        "https://www.inegi.org.mx",
        "https://www.cdc.gov"
    ]
    
    results = []
    for url in official_seeds:
        if len(results) >= limit:
            break
            
        if not is_official(url):
            continue
            
        print(f"  📡 Consultando: {url}")
        content = fetch_content(url)
        
        if topic.lower() in content.lower():
            # Extraer snippet relevante
            sentences = content.split(".")
            relevant = next((s.strip() for s in sentences if topic.lower() in s.lower()), content[:300])
            
            results.append({
                "fuente": url,
                "dato": relevant.strip(),
                "fecha_consulta": datetime.now().isoformat(),
                "verificado": True
            })
            print(f"  ✅ Datos encontrados en {url}")
    
    # Guardar fuentes verificadas
    df = pd.DataFrame(results)
    df.to_csv(f"{OUTDIR}/fuentes.csv", index=False, encoding='utf-8')
    print(f"📊 {len(results)} fuentes oficiales guardadas en fuentes.csv")
    
    return results

def generate_script_storyboard(sources, topic):
    """FASE 1 y 2: Generar guion y storyboard"""
    print("📝 FASE 1-2: Generando guion y storyboard...")
    
    sources_text = "\n".join([f"- {s['fuente']}: {s['dato']}" for s in sources])
    
    prompt = f"""Eres un creador de contenido educativo para CO-RA (Ecosistema Cognitivo Inclusivo).

TEMA: {topic}

FUENTES OFICIALES VERIFICADAS:
{sources_text}

Crea un video educativo usando ÚNICAMENTE estos datos oficiales.

Devuelve JSON con:
- "script": Texto de narración (máximo 120 palabras, tono educativo y accesible)
- "scenes": Array de 4-6 escenas con formato [{{"n":1, "visual":"descripción visual detallada para imagen realista 1080p"}}]

El video debe ser:
- Educativo y basado en hechos
- Accesible para diferentes capacidades
- Visualmente claro y profesional
- Coherente con la misión inclusiva de CO-RA"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        plan = json.loads(response.choices[0].message.content)
        
        # Guardar plan
        with open(f"{OUTDIR}/plan.json", "w", encoding="utf-8") as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Guion generado: {len(plan['script'].split())} palabras")
        print(f"✅ Storyboard: {len(plan['scenes'])} escenas")
        
        return plan
        
    except Exception as e:
        print(f"❌ Error generando guion: {e}")
        return None

def generate_scene_images(scenes):
    """FASE 3: Generación visual con DALL-E"""
    print("🎨 FASE 3: Generando imágenes para cada escena...")
    
    image_paths = []
    
    for scene in scenes:
        try:
            print(f"  🖼️  Generando escena {scene['n']}: {scene['visual'][:50]}...")
            
            # Prompt optimizado para DALL-E
            visual_prompt = f"Imagen educativa profesional 1080p, estilo documental, {scene['visual']}, iluminación natural, colores claros y accesibles"
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=visual_prompt,
                size="1792x1024",  # Aspect ratio 16:9
                quality="standard",
                n=1
            )
            
            # Descargar imagen
            image_url = response.data[0].url
            img_response = requests.get(image_url)
            
            if img_response.status_code == 200:
                image_path = f"{OUTDIR}/scene_{scene['n']:02d}.png"
                with open(image_path, "wb") as f:
                    f.write(img_response.content)
                
                image_paths.append(image_path)
                print(f"  ✅ Escena {scene['n']} guardada")
            
        except Exception as e:
            print(f"  ❌ Error generando escena {scene['n']}: {e}")
            # Crear imagen placeholder si falla
            placeholder_path = f"{OUTDIR}/scene_{scene['n']:02d}_placeholder.png"
            image_paths.append(placeholder_path)
    
    return image_paths

def generate_voiceover(script_text):
    """FASE 4: Generar locución con TTS"""
    print("🎤 FASE 4: Generando locución...")
    
    try:
        voice_path = f"{OUTDIR}/voz.mp3"
        
        response = client.audio.speech.create(
            model="tts-1-hd",
            voice="nova",  # Voz femenina clara
            input=script_text,
            speed=0.9  # Ligeramente más lento para accesibilidad
        )
        
        with open(voice_path, "wb") as f:
            f.write(response.read())
        
        print("✅ Locución generada")
        return voice_path
        
    except Exception as e:
        print(f"❌ Error generando locución: {e}")
        return None

def assemble_video(image_paths, voice_path, background_music=None):
    """FASE 5: Montaje y edición final"""
    print("🎬 FASE 5: Montaje final del video...")
    
    try:
        # Cargar audio principal
        voice_audio = AudioFileClip(voice_path)
        duration_per_scene = voice_audio.duration / len(image_paths)
        
        # Crear clips de imagen
        video_clips = []
        for img_path in image_paths:
            if os.path.exists(img_path):
                clip = ImageClip(img_path).set_duration(duration_per_scene).resize((1920, 1080))
                video_clips.append(clip)
        
        # Concatenar video
        final_video = concatenate_videoclips(video_clips, method="compose")
        
        # Preparar audio final
        if background_music and os.path.exists(background_music):
            # Añadir música de fondo
            bg_audio = AudioFileClip(background_music).volumex(0.15)  # Volumen bajo
            
            # Ajustar duración de música de fondo
            if bg_audio.duration < voice_audio.duration:
                loops_needed = math.ceil(voice_audio.duration / bg_audio.duration)
                bg_audio = concatenate_audioclips([bg_audio] * loops_needed).set_duration(voice_audio.duration)
            else:
                bg_audio = bg_audio.set_duration(voice_audio.duration)
            
            final_audio = CompositeAudioClip([voice_audio, bg_audio])
        else:
            final_audio = voice_audio
        
        # Normalizar audio
        final_audio = final_audio.fx(afx.audio_normalize)
        
        # Exportar video final
        output_path = f"{OUTDIR}/video_final.mp4"
        final_video.set_audio(final_audio).write_videofile(
            output_path,
            fps=30,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True
        )
        
        print(f"✅ Video final exportado: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Error en montaje: {e}")
        return None

def autopilot_video_generator(topic):
    """Orquestador principal - Ejecuta las 6 fases completas"""
    print("🚀 INICIANDO GENERADOR AUTOMÁTICO DE VIDEOS CO-RA")
    print("=" * 60)
    
    # FASE 0: Investigación oficial
    sources = harvest_official_data(topic)
    if not sources:
        print("❌ No se encontraron fuentes oficiales suficientes")
        return False
    
    # FASE 1-2: Guion y Storyboard
    plan = generate_script_storyboard(sources, topic)
    if not plan:
        return False
    
    # FASE 3: Generación visual
    images = generate_scene_images(plan["scenes"])
    
    # FASE 4: Locución
    voice = generate_voiceover(plan["script"])
    if not voice:
        return False
    
    # FASE 5: Montaje
    bg_music = os.getenv("BGMUSIC_PATH")
    video_path = assemble_video(images, voice, bg_music)
    
    # FASE 6: Finalización
    if video_path:
        print("\n🎉 GENERACIÓN COMPLETADA")
        print("=" * 60)
        print(f"📁 Archivos generados en: {OUTDIR}/")
        print(f"📊 fuentes.csv - Fuentes oficiales verificadas")
        print(f"📝 plan.json - Guion y storyboard")
        print(f"🎬 video_final.mp4 - Video listo para publicar")
        return True
    
    return False

if __name__ == "__main__":
    # Ejemplo de uso
    topic = "Impacto del cambio climático en México 2025"
    autopilot_video_generator(topic)