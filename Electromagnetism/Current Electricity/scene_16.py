from common import *


class Scene16Capacitance(Lesson):
    def construct(self):
        self.begin(16,'السعة الكهربائية','ماذا تعني سعة أكبر عند الجهد نفسه؟')
        c1=capacitor(np.array([-3.2,.3,0]),height=1.3,gap=1.3,n=4)
        c2=capacitor(np.array([3.2,.3,0]),height=2.6,gap=1.3,n=8)
        self.show(c1,c2,eq('V = 6 V',29,VOLT).move_to([-3.2,2.25,0]),eq('V = 6 V',29,VOLT).move_to([3.2,2.25,0]))
        self.show(eq('C₁ = 1 μF',30,VOLT).move_to([-3.2,-1.4,0]),eq('C₂ = 2 μF',30,VOLT).move_to([3.2,-1.4,0]))
        self.say('المسافة والعازل ثابتان وتضاعفت مساحة اللوحين',5)
        self.formula('C = Q / V    •    Q = CV',VOLT,y=-2.3)
        self.say('الشحنة هنا مقدار الشحنة على لوح واحد، وليست مجموع اللوحين',5)
        self.clear_stage()
        self.show(panel(5.6,3.4,[-3.1,.5,0]),panel(5.6,3.4,[3.1,.5,0]))
        self.show(label_pair('المكثف الأول','Q₁ = 1 μF × 6 V = 6 μC',CURRENT).move_to([-3.1,.6,0]),
                  label_pair('المكثف الثاني','Q₂ = 2 μF × 6 V = 12 μC',CURRENT).move_to([3.1,.6,0]))
        self.say('عند الجهد نفسه: مضاعفة السعة تعني مضاعفة الشحنة',5)
        self.formula('1 F = 1 C/V    •    1 μF = 10⁻⁶ F',VOLT)
        self.say(
            'تعتمد السعة الكهربائية على شكل الموصلات وحجمها وأبعادها وترتيبها والمسافات بينها، وكذلك على نوع المادة العازلة',
            5)
        self.finish('السعة تحدد الشحنة على كل لوح عند جهد معلوم','C = Q / V',VOLT)


if __name__=='__main__': render_scene(Scene16Capacitance)
