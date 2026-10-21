"""S05 — Zero net flux does not mean zero field.

Run this file directly from PyCharm. Optional narration assets beside this file:
 S05_ar.wav (one complete recording), OR
 S05_B01_ar.wav, S05_B02_ar.wav, S05_B03_ar.wav.
The complete recording uses planned paragraph starts; for precise syncing to an
unsegmented recording, adjust PARAGRAPH_STARTS from measured speech timestamps.
"""
from __future__ import annotations

from pathlib import Path
from html import escape
import contextlib
import subprocess
import sys
import wave
import numpy as np
from manim import *

DARK = '#101820'
WHITEISH = '#F5F5F5'
GOLD = '#F6C85F'
CYAN = '#58C4DD'
VIOLET = '#C792EA'
RED = '#FF6B6B'
BLUE = '#64B5F6'
ARABIC_FONT = 'Arial'  # Set to an Arabic-shaping-capable font installed on your PC.
PARAGRAPH_STARTS = (1.0, 20.0, 41.0)
FADE_LAST_HALF_SECOND = True


def wav_seconds(path: Path) -> float:
    if not path.is_file():
        return 0.0
    try:
        with contextlib.closing(wave.open(str(path), 'rb')) as f:
            return f.getnframes() / f.getframerate()
    except (wave.Error, OSError, ZeroDivisionError):
        return 0.0


class GaussScene05(Scene):
    def construct(self):
        self.camera.background_color = DARK
        self.elapsed = 0.0
        self.directory = Path(__file__).resolve().parent
        self.planned = [(16., 3.), (18., 3.), (19., 4.)]
        self.lengths = [sum(x) for x in self.planned]  # 19 + 21 + 23 = 63
        self.audio_mode = 'silent'
        self.audio_paths = []
        whole = self.directory / 'S05_ar.wav'
        clips = [self.directory / f'S05_B0{i}_ar.wav' for i in (1, 2, 3)]
        if whole.is_file():
            self.audio_mode = 'whole'
            self.audio_paths = [whole]
            extra = max(0., wav_seconds(whole) - 59.)
            # The planned 1s silent lead-in plus the last 4s reading hold.
            # Keep the first two paragraph start times unchanged with whole audio.
            self.lengths[-1] += extra
            print('S05 whole audio:', round(wav_seconds(whole), 2), 'seconds; '
                  'paragraph cues use the planned offsets', PARAGRAPH_STARTS)
        elif all(p.is_file() for p in clips):
            self.audio_mode = 'beats'
            self.audio_paths = clips
            self.lengths = [max(speech, wav_seconds(p)) + hold
                            for p, (speech, hold) in zip(clips, self.planned)]
        else:
            print('S05: no complete set of narration files; silent preview.')
        self.scene_length = 1.0 + sum(self.lengths)
        print('S05 planned/adjusted duration:', round(self.scene_length, 3), 's')

        self.make_objects()
        self.play_for(FadeIn(self.title, shift=DOWN * .12), 0.8)
        self.pause(.2)
        if self.audio_mode == 'whole':
            self.add_sound(str(self.audio_paths[0]))

        self.beat1()
        self.beat2()
        self.beat3()
        assert abs(self.elapsed - self.scene_length) < 0.06, (self.elapsed, self.scene_length)

    def ar(self, message, size=27, color=WHITEISH):
        # MarkupText uses Pango's markup renderer, which correctly shapes these
        # Arabic strings; Text can produce an empty SVG on this installation.
        return MarkupText(escape(message), font=ARABIC_FONT, font_size=size, color=color)

    def make_objects(self):
        self.title = self.ar('صفرية التدفق الصافي لا تعني انعدام المجال', 39)
        self.title.move_to(UP * 3.28)

        # A perspective schematic of a closed 3D cuboid: 2D section is NOT
        # mistaken for the mathematical integration surface.
        # The visible front projection lies approximately in [-5.65,-2.20].
        x0, x1 = -5.75, -2.65
        y0, y1 = -1.25, 1.30
        offset = np.array([.58, .44, 0.])
        fbl = np.array([x0,y0,0]); fbr=np.array([x1,y0,0])
        ftr = np.array([x1,y1,0]); ftl=np.array([x0,y1,0])
        bbl=fbl+offset; bbr=fbr+offset; btr=ftr+offset; btl=ftl+offset
        self.box_edges = VGroup()
        for a,b in [(fbl,fbr),(fbr,ftr),(ftr,ftl),(ftl,fbl),
                    (fbl,bbl),(fbr,bbr),(ftr,btr),(ftl,btl),
                    (bbl,bbr),(bbr,btr),(btr,btl),(btl,bbl)]:
            self.box_edges.add(Line(a,b, color=CYAN, stroke_width=2.5,
                                    stroke_opacity=.65 if a[0] != b[0] else .9))
        self.left_face = Polygon(fbl, ftl, btl, bbl, stroke_width=3, color=CYAN,
                                 fill_color=CYAN, fill_opacity=.10)
        self.right_face = Polygon(fbr, ftr, btr, bbr, stroke_width=3, color=CYAN,
                                  fill_color=CYAN, fill_opacity=.10)
        self.other_faces = VGroup(
            Polygon(fbl,fbr,ftr,ftl,stroke_width=0,fill_color=CYAN,fill_opacity=.035),
            Polygon(ftl,ftr,btr,btl,stroke_width=0,fill_color=CYAN,fill_opacity=.07),
            Polygon(fbl,fbr,bbr,bbl,stroke_width=0,fill_color=CYAN,fill_opacity=.07),
            Polygon(bbl,bbr,btr,btl,stroke_width=0,fill_color=CYAN,fill_opacity=.02),
        )
        self.box_name = self.ar('صندوق مغلق', 26).move_to([-4.0,-2.10,0])
        self.field_label = self.ar('مجال منتظم', 26, GOLD).move_to([-4.02,2.30,0])

        # All field vectors point in +x with equal size. Their rays extend
        # on either side of the closed box, signalling the field is external.
        self.field_lines = VGroup()
        for yy in [-1.65,-.85,0,.85,1.65]:
            for xx in [-6.0, -3.7]:
                self.field_lines.add(Arrow([xx,yy,0], [xx+1.5,yy,0], buff=0,
                    color=GOLD, stroke_width=3.8,
                    max_tip_length_to_length_ratio=.12))
        self.left_normal = Arrow([-5.83,.05,0],[-6.10,.05,0],buff=0,
                                 color=VIOLET,stroke_width=5)
        self.right_normal = Arrow([-2.03,.05,0],[-1.25,.05,0],buff=0,
                                  color=VIOLET,stroke_width=5)
        self.left_n_label = MathTex(r'\hat{\mathbf n}',color=VIOLET,font_size=29).next_to(self.left_normal,UP,buff=.12)
        self.right_n_label = MathTex(r'\hat{\mathbf n}',color=VIOLET,font_size=29).next_to(self.right_normal,UP,buff=.12)
        self.left_A = MathTex('A',font_size=31,color=WHITEISH).move_to([-5.93,-.55,0])
        self.right_A = MathTex('A',font_size=31,color=WHITEISH).move_to([-2.12,-.6,0])
        self.left_face_label = self.ar('الوجه الأيسر',25).move_to([-5.0,-2.65,0])
        self.right_face_label = self.ar('الوجه الأيمن',25).move_to([-2.15,-2.65,0])
        self.question = self.ar('لا توجد شحنة في الداخل: هل يتلاشى المجال بالضرورة؟؟', 23)
        self.question.move_to([3.55,1.30,0]); self.question.scale_to_fit_width(5.6)
        self.no = self.ar('لا', 36, RED).move_to([3.55,.80,0])

        self.left_flux = MathTex(r'\Phi_{\mathrm{left}}=-E_0A',color=WHITEISH,font_size=37)
        self.right_flux = MathTex(r'\Phi_{\mathrm{right}}=+E_0A',color=WHITEISH,font_size=37)
        self.other_flux = MathTex(r'\Phi_{\mathrm{other\ faces}}=0',color=WHITEISH,font_size=34)
        self.conclusion = MathTex(
            r'\Phi_E=0\quad\text{while}\quad\mathbf E=E_0\hat{\mathbf x}\ne\mathbf 0',
            color=WHITEISH,font_size=35)
        for mob, yy in [(self.left_flux,.10),(self.right_flux,-.58),(self.other_flux,-1.28),(self.conclusion,-2.25)]:
            mob.move_to([3.36, yy, 0])
            mob.scale_to_fit_width(min(mob.width,5.25))
        self.other_face_label=self.ar('الأوجه الأخرى: لا يوجد تدفق، نظراً لأنها موازية للمجال.',24).move_to([3.3,1.22,0])
        self.nonzero_label=self.ar('مجال غير صفري',25,GOLD).move_to([3.3,1.85,0])
        # Keep labels and arrows separate to avoid clipping/overlaps.

    def beat_start(self, i):
        if self.audio_mode == 'beats':
            self.add_sound(str(self.audio_paths[i]))
        self.beat_end = self.elapsed + self.lengths[i]

    def play_for(self, animation, seconds):
        self.play(animation, run_time=seconds)
        self.elapsed += seconds

    def pause(self, seconds):
        if seconds > 1e-5:
            self.wait(seconds); self.elapsed += seconds

    def finish_beat(self, final=False):
        left = self.beat_end - self.elapsed
        if left < -.05:
            raise RuntimeError(f'S05 beat exceeded schedule by {-left:.2f}s')
        if final and FADE_LAST_HALF_SECOND and left >= .5:
            self.pause(left-.5)
            self.play_for(FadeOut(Group(*list(self.mobjects))),.5)
        else:
            self.pause(max(0.,left))

    def beat1(self):
        self.beat_start(0)
        self.play_for(LaggedStart(*[GrowArrow(a) for a in self.field_lines],lag_ratio=.07), 2.0)
        self.play_for(FadeIn(self.field_label),.6)
        self.play_for(Create(self.box_edges),1.5)
        self.play_for(FadeIn(self.other_faces),.5)
        self.play_for(FadeIn(self.box_name),.6)
        # The field remains visibly present while no charge is shown inside.
        self.play_for(Indicate(self.field_label,color=GOLD,scale_factor=1.08),1.0)
        self.play_for(Indicate(self.box_edges,color=CYAN,scale_factor=1.015),1.0)
        # Hold question for exactly the last three seconds of this beat.
        self.pause(max(0.,self.beat_end-self.elapsed-3.0))
        self.play_for(FadeIn(self.question),.65)
        self.pause(2.35)
        self.finish_beat()

    def beat2(self):
        self.beat_start(1)
        self.play_for(FadeIn(self.no),.5)
        self.play_for(FadeIn(self.left_face),.6)
        self.play_for(GrowArrow(self.left_normal),.8)
        self.play_for(AnimationGroup(FadeIn(self.left_n_label), FadeIn(self.left_A),
                                     FadeIn(self.left_face_label)), .8)
        self.play_for(Write(self.left_flux),1.2)
        self.play_for(Indicate(self.left_flux,color=RED,scale_factor=1.04),.8)
        self.play_for(FadeIn(self.right_face),.6)
        self.play_for(GrowArrow(self.right_normal),.8)
        self.play_for(AnimationGroup(FadeIn(self.right_n_label), FadeIn(self.right_A),
                                     FadeIn(self.right_face_label)), .8)
        self.play_for(Write(self.right_flux),1.2)
        self.play_for(Indicate(self.right_flux,color=CYAN,scale_factor=1.04),.8)
        self.play_for(Circumscribe(VGroup(self.left_flux,self.right_flux),color=WHITEISH),1.2)
        self.finish_beat()

    def beat3(self):
        self.beat_start(2)
        self.play_for(FadeOut(self.question,self.no),.5)
        self.play_for(FadeIn(self.other_face_label),.5)
        self.play_for(Indicate(self.other_faces,color=CYAN,scale_factor=1.02),1.2)
        self.play_for(Write(self.other_flux),1.2)
        self.play_for(Indicate(self.other_flux,color=CYAN),.8)
        self.play_for(Write(self.conclusion),1.6)
        self.play_for(FadeIn(self.nonzero_label),.7)
        self.play_for(Indicate(self.field_lines,color=GOLD,scale_factor=1.015),1.1)
        self.play_for(Circumscribe(self.conclusion,color=WHITEISH),1.4)
        self.finish_beat(final=True)


# ===============================================================
# RENDER — CLICK RUN IN PYCHARM; OPEN COMPLETED VIDEO AUTOMATICALLY
# ===============================================================
if __name__ == '__main__':
    subprocess.run([
        sys.executable, '-m', 'manim', '-p', '-qh',
        '-r', '1920,1080', '--fps', '30',
        str(Path(__file__).resolve()), 'GaussScene05',
    ], check=True)
