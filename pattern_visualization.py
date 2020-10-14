import ast
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math

# Leer el archivo reporte de patrones generado por patminer
# Cambiar el nombre y la ubicacion del .txt
with open('ExtractedPatterns//Tipo_de_contratacion.txt', encoding='utf-8-sig') as file:
    file_contents = file.read()
# Nombre del Feature / Carpeta donde se guardaran los patrones
featurename = 'TipoDeContratacion'

# Encontrar la cuenta de clases
class_index = 0
class_loc = []

while class_index != -1:
    loc = class_index + 1
    class_index = file_contents.find('Class: {', loc)
    if class_index != -1:
        class_loc.append(class_index)

# Por cada clase encontrada en el patrón
for y in range(len(class_loc)):

    class_name_start = file_contents.find('{', class_loc[y])
    class_name_end = file_contents.find('}', class_loc[y])
    class_name = file_contents[class_name_start+1:class_name_end]

    class_nb = class_name.find('\'')
    class_short_name = class_name[class_nb+1:-1]

    if class_short_name == '?':
        class_short_name = 'Otro'

    ps_index = 0
    patt_loc = []

    while ps_index != -1:
        loc = ps_index + 1
        ps_index = file_contents.find('Pattern: {', loc, class_loc[1])
        if ps_index != -1:
            patt_loc.append(ps_index)


    # Obtener listas de patrones y sus caracteristicas
    patt_list = []
    count_list = []
    tsupport_list = []
    dsupport_list = []
    conf_list = []

    for i in range(len(patt_loc)):
        start = patt_loc[i]
        if i == len(patt_loc) - 1:
            end = len(file_contents)
        else:
            end = patt_loc[i + 1] - 1
        
        openb_loc = file_contents.find('{', start, end)
        closeb_loc = file_contents.find('}', start, end)
        
        open_count_loc = file_contents.find('[', start, end)
        close_count_loc = file_contents.find(']', start, end)

        open_tsupp_loc = file_contents.find('[', close_count_loc+1, end)
        close_tsupp_loc = file_contents.find(']', close_count_loc+1, end)

        open_dsupp_loc = file_contents.find('Dataset\'s support: ', close_tsupp_loc+1, end)
        close_dsupp_loc = file_contents.find('%', close_tsupp_loc+1, end)

        open_conf_loc = file_contents.find('Confidence: ', close_dsupp_loc+1, end)
        close_conf_loc = file_contents.find('%', close_dsupp_loc+1, end)


        patt_list.append((openb_loc, closeb_loc))
        count_list.append((open_count_loc, close_count_loc+1))
        tsupport_list.append((open_tsupp_loc, close_tsupp_loc+1))
        dsupport_list.append((open_dsupp_loc+19, close_dsupp_loc+1))
        conf_list.append((open_conf_loc+12, close_conf_loc+1))

    # Dividir los patrones por numeros de features
    patt_list_1 = []
    patt_list_2 = []
    patt_list_3 = []
    patt_list_4 = []
    i_list_1 = []
    i_list_2 = []
    i_list_3 = []
    i_list_4 = []

    for i in range(len(patt_list)):
        s = patt_list[i][0]
        e = patt_list[i][1]
        pattern = file_contents[s+1:e]
        pattern_words = pattern.split()
        and_instances = 0
        for w in pattern_words:
            if w == 'AND':
                and_instances += 1
        
        if and_instances == 0:
            patt_list_1.append((s+1,e))
            i_list_1.append(i)
        elif and_instances == 1:
            patt_list_2.append((s+1,e))
            i_list_2.append(i)
        elif and_instances == 2:
            patt_list_3.append((s+1,e))
            i_list_3.append(i)
        elif and_instances == 3:
            patt_list_4.append((s+1,e))
            i_list_4.append(i)
    
    # Dividir el resto de los elementos
    count_list_1 = []
    count_list_2 = []
    count_list_3 = []
    count_list_4 = []

    tsupport_list_1 = []
    tsupport_list_2 = []
    tsupport_list_3 = []
    tsupport_list_4 = []

    dsupport_list_1 = []
    dsupport_list_2 = []
    dsupport_list_3 = []
    dsupport_list_4 = []

    conf_list_1 = []
    conf_list_2 = []
    conf_list_3 = []
    conf_list_4 = []

    for x in i_list_1:
        count_list_1.append(count_list[x])
        tsupport_list_1.append(tsupport_list[x])
        dsupport_list_1.append(dsupport_list[x])
        conf_list_1.append(conf_list[x])

    for x in i_list_2:
        count_list_2.append(count_list[x])
        tsupport_list_2.append(tsupport_list[x])
        dsupport_list_2.append(dsupport_list[x])
        conf_list_2.append(conf_list[x])

    for x in i_list_3:
        count_list_3.append(count_list[x])
        tsupport_list_3.append(tsupport_list[x])
        dsupport_list_3.append(dsupport_list[x])
        conf_list_3.append(conf_list[x])

    for x in i_list_4:
        count_list_4.append(count_list[x])
        tsupport_list_4.append(tsupport_list[x])
        dsupport_list_4.append(dsupport_list[x])
        conf_list_4.append(conf_list[x])


    # Visualizar patrones de 1 feature
    for i in range(len(patt_list_1)):
        title1 = f'TARGET CLASS: {class_name}'
        pattern_name = f'Pattern: {file_contents[patt_list_1[i][0]:patt_list_1[i][1]]}'
        title2 = f'COMPLEMENT OF TARGET CLASS: {class_name}'

        raw_count = file_contents[count_list_1[i][0]:count_list_1[i][1]]
        count_list = ast.literal_eval(raw_count)
        
        raw_class_support = file_contents[tsupport_list_1[i][0]:tsupport_list_1[i][1]]
        class1_end = raw_class_support.find('%, ')
        class1_support = float(raw_class_support[1:class1_end])
        class2_end = raw_class_support.find('%]')
        class2_support = float(raw_class_support[class1_end+3:class2_end])
        
        try:
            class1_members = round(count_list[0]/(class1_support/100.0))
        except:
            class1_members = 0
        try:
            class2_members = round(count_list[1]/(class2_support/100.0))
        except:
            class2_members = 0

        universe_members = class1_members + class2_members
        class1_percentage = (class1_members / universe_members)*100
        class2_percentage = (class2_members / universe_members)*100
        universe_radius = 1.0

        class1_radius = math.sqrt(class1_members / universe_members)
        class2_radius = math.sqrt(class2_members / universe_members)
        try:
            pattern1_members = round(class1_members  * (class1_support/100.0))
        except:
            pattern1_members = 0
        try:
            pattern2_members = round(class2_members  * (class2_support/100.0))
        except:
            pattern2_members = 0

        pattern1_radius = math.sqrt(pattern1_members / universe_members)
        pattern2_radius = math.sqrt(pattern2_members / universe_members)


        # TARGET CLASS VISUALIZATION
        circle1 = plt.Circle((0.5, 0.5), universe_radius, color='r', clip_on=False)
        circle2 = plt.Circle((0.5, 0.5), class1_radius, color='blue', clip_on=False)
        circle3 = plt.Circle((0.5, 0.5), pattern1_radius, color='g', clip_on=False)

        fig, ax = plt.subplots()
        ax.add_artist(circle1)
        ax.add_artist(circle2)
        ax.add_artist(circle3)

        
        textstr1 = title1
        textstr2 = pattern_name
        textstr3 = f'Confidence: {file_contents[conf_list_1[i][0]:conf_list_1[i][1]]}\nDataset\'s Support: {file_contents[dsupport_list_1[i][0]:dsupport_list_1[i][1]]}'
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(-0.75, 1.60, textstr1, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        ax.text(-0.75, -0.65, textstr2, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        ax.text(1.25, -0.45, textstr3, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        

        red_circle = mpatches.Patch(color='r', label=f'Total Data = {universe_members}')
        blue_circle = mpatches.Patch(color='blue', label=f'Class Size = {round(class1_percentage,2)}% of the total data')
        green_circle = mpatches.Patch(color='g', label=f'Pattern Support Size = {round(class1_support,2)}% of the class size')

        plt.legend(handles=[red_circle, blue_circle, green_circle], bbox_to_anchor=(1.75, 1.5))

        plt.axis('off')
        filename = f'Visualization//{featurename}//{class_short_name}//01_Features//{i}_TargetClass.png'
        plt.ioff()
        plt.savefig(filename, bbox_inches='tight')
        
        # COMPLEMENT CLASS VISUALIZATION
        circle1 = plt.Circle((0.5, 0.5), universe_radius, color='r', clip_on=False)
        circle2 = plt.Circle((0.5, 0.5), class2_radius, color='blue', clip_on=False)
        circle3 = plt.Circle((0.5, 0.5), pattern2_radius, color='g', clip_on=False)

        fig, ax = plt.subplots()
        ax.add_artist(circle1)
        ax.add_artist(circle2)
        ax.add_artist(circle3)

        textstr1 = title2
        textstr2 = pattern_name
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(-0.75, 1.60, textstr1, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        ax.text(-0.75, -0.65, textstr2, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        ax.text(1.25, -0.45, textstr3, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)

        red_circle = mpatches.Patch(color='r', label=f'Total Data = {universe_members}')
        blue_circle = mpatches.Patch(color='blue', label=f'Class Size = {round(class2_percentage,2)}% of the total data')
        green_circle = mpatches.Patch(color='g', label=f'Pattern Support Size = {round(class2_support,2)}% of the class size')

        plt.legend(handles=[red_circle, blue_circle, green_circle], bbox_to_anchor=(1.75, 1.5))

        plt.axis('off')
        filename = f'Visualization//{featurename}//{class_short_name}//01_Features//{i}_ComplementaryClass.png'
        plt.ioff()
        plt.savefig(filename, bbox_inches='tight')


    # Visualizar patrones de 2 features
    for i in range(len(patt_list_2)):
        title1 = f'TARGET CLASS: {class_name}'
        pattern_name = f'Pattern: {file_contents[patt_list_2[i][0]:patt_list_2[i][1]]}'
        title2 = f'COMPLEMENT OF TARGET CLASS: {class_name}'

        raw_count = file_contents[count_list_2[i][0]:count_list_2[i][1]]
        count_list = ast.literal_eval(raw_count)
        
        raw_class_support = file_contents[tsupport_list_2[i][0]:tsupport_list_2[i][1]]
        class1_end = raw_class_support.find('%, ')
        class1_support = float(raw_class_support[1:class1_end])
        class2_end = raw_class_support.find('%]')
        class2_support = float(raw_class_support[class1_end+3:class2_end])
        
        try:
            class1_members = round(count_list[0]/(class1_support/100.0))
        except:
            class1_members = 0
        try:
            class2_members = round(count_list[1]/(class2_support/100.0))
        except:
            class2_members = 0

        universe_members = class1_members + class2_members
        class1_percentage = (class1_members / universe_members)*100
        class2_percentage = (class2_members / universe_members)*100
        universe_radius = 1.0

        class1_radius = math.sqrt(class1_members / universe_members)
        class2_radius = math.sqrt(class2_members / universe_members)
        try:
            pattern1_members = round(class1_members  * (class1_support/100.0))
        except:
            pattern1_members = 0
        try:
            pattern2_members = round(class2_members  * (class2_support/100.0))
        except:
            pattern2_members = 0

        pattern1_radius = math.sqrt(pattern1_members / universe_members)
        pattern2_radius = math.sqrt(pattern2_members / universe_members)


        # TARGET CLASS VISUALIZATION
        circle1 = plt.Circle((0.5, 0.5), universe_radius, color='r', clip_on=False)
        circle2 = plt.Circle((0.5, 0.5), class1_radius, color='blue', clip_on=False)
        circle3 = plt.Circle((0.5, 0.5), pattern1_radius, color='g', clip_on=False)

        fig, ax = plt.subplots()
        ax.add_artist(circle1)
        ax.add_artist(circle2)
        ax.add_artist(circle3)

        
        textstr1 = title1
        textstr2 = pattern_name
        textstr3 = f'Confidence: {file_contents[conf_list_2[i][0]:conf_list_2[i][1]]}\nDataset\'s Support: {file_contents[dsupport_list_2[i][0]:dsupport_list_2[i][1]]}'
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(-0.75, 1.60, textstr1, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        ax.text(-0.75, -0.65, textstr2, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        ax.text(1.25, -0.45, textstr3, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        

        red_circle = mpatches.Patch(color='r', label=f'Total Data = {universe_members}')
        blue_circle = mpatches.Patch(color='blue', label=f'Class Size = {round(class1_percentage,2)}% of the total data')
        green_circle = mpatches.Patch(color='g', label=f'Pattern Support Size = {round(class1_support,2)}% of the class size')

        plt.legend(handles=[red_circle, blue_circle, green_circle], bbox_to_anchor=(1.75, 1.5))

        plt.axis('off')
        filename = f'Visualization//{featurename}//{class_short_name}//02_Features//{i}_TargetClass.png'
        plt.ioff()
        plt.savefig(filename, bbox_inches='tight')
        
        # COMPLEMENT CLASS VISUALIZATION
        circle1 = plt.Circle((0.5, 0.5), universe_radius, color='r', clip_on=False)
        circle2 = plt.Circle((0.5, 0.5), class2_radius, color='blue', clip_on=False)
        circle3 = plt.Circle((0.5, 0.5), pattern2_radius, color='g', clip_on=False)

        fig, ax = plt.subplots()
        ax.add_artist(circle1)
        ax.add_artist(circle2)
        ax.add_artist(circle3)

        textstr1 = title2
        textstr2 = pattern_name
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(-0.75, 1.60, textstr1, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        ax.text(-0.75, -0.65, textstr2, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        ax.text(1.25, -0.45, textstr3, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)

        red_circle = mpatches.Patch(color='r', label=f'Total Data = {universe_members}')
        blue_circle = mpatches.Patch(color='blue', label=f'Class Size = {round(class2_percentage,2)}% of the total data')
        green_circle = mpatches.Patch(color='g', label=f'Pattern Support Size = {round(class2_support,2)}% of the class size')

        plt.legend(handles=[red_circle, blue_circle, green_circle], bbox_to_anchor=(1.75, 1.5))

        plt.axis('off')
        filename = f'Visualization//{featurename}//{class_short_name}//02_Features//{i}_ComplementaryClass.png'
        plt.ioff()
        plt.savefig(filename, bbox_inches='tight')

    # # Visualizar patrones de 3 features
    for i in range(len(patt_list_3)):
        title1 = f'TARGET CLASS: {class_name}'
        pattern_name = f'Pattern: {file_contents[patt_list_3[i][0]:patt_list_3[i][1]]}'
        title2 = f'COMPLEMENT OF TARGET CLASS: {class_name}'

        raw_count = file_contents[count_list_3[i][0]:count_list_3[i][1]]
        count_list = ast.literal_eval(raw_count)
        
        raw_class_support = file_contents[tsupport_list_3[i][0]:tsupport_list_3[i][1]]
        class1_end = raw_class_support.find('%, ')
        class1_support = float(raw_class_support[1:class1_end])
        class2_end = raw_class_support.find('%]')
        class2_support = float(raw_class_support[class1_end+3:class2_end])
        
        try:
            class1_members = round(count_list[0]/(class1_support/100.0))
        except:
            class1_members = 0
        try:
            class2_members = round(count_list[1]/(class2_support/100.0))
        except:
            class2_members = 0

        universe_members = class1_members + class2_members
        class1_percentage = (class1_members / universe_members)*100
        class2_percentage = (class2_members / universe_members)*100
        universe_radius = 1.0

        class1_radius = math.sqrt(class1_members / universe_members)
        class2_radius = math.sqrt(class2_members / universe_members)
        try:
            pattern1_members = round(class1_members  * (class1_support/100.0))
        except:
            pattern1_members = 0
        try:
            pattern2_members = round(class2_members  * (class2_support/100.0))
        except:
            pattern2_members = 0

        pattern1_radius = math.sqrt(pattern1_members / universe_members)
        pattern2_radius = math.sqrt(pattern2_members / universe_members)


        # TARGET CLASS VISUALIZATION
        circle1 = plt.Circle((0.5, 0.5), universe_radius, color='r', clip_on=False)
        circle2 = plt.Circle((0.5, 0.5), class1_radius, color='blue', clip_on=False)
        circle3 = plt.Circle((0.5, 0.5), pattern1_radius, color='g', clip_on=False)

        fig, ax = plt.subplots()
        ax.add_artist(circle1)
        ax.add_artist(circle2)
        ax.add_artist(circle3)

        
        textstr1 = title1
        textstr2 = pattern_name
        textstr3 = f'Confidence: {file_contents[conf_list_3[i][0]:conf_list_3[i][1]]}\nDataset\'s Support: {file_contents[dsupport_list_3[i][0]:dsupport_list_3[i][1]]}'
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(-0.75, 1.60, textstr1, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        ax.text(-0.75, -0.65, textstr2, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        ax.text(1.25, -0.45, textstr3, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        

        red_circle = mpatches.Patch(color='r', label=f'Total Data = {universe_members}')
        blue_circle = mpatches.Patch(color='blue', label=f'Class Size = {round(class1_percentage,2)}% of the total data')
        green_circle = mpatches.Patch(color='g', label=f'Pattern Support Size = {round(class1_support,2)}% of the class size')

        plt.legend(handles=[red_circle, blue_circle, green_circle], bbox_to_anchor=(1.75, 1.5))

        plt.axis('off')
        filename = f'Visualization//{featurename}//{class_short_name}//03_Features//{i}_TargetClass.png'
        plt.ioff()
        plt.savefig(filename, bbox_inches='tight')
        
        # COMPLEMENT CLASS VISUALIZATION
        circle1 = plt.Circle((0.5, 0.5), universe_radius, color='r', clip_on=False)
        circle2 = plt.Circle((0.5, 0.5), class2_radius, color='blue', clip_on=False)
        circle3 = plt.Circle((0.5, 0.5), pattern2_radius, color='g', clip_on=False)

        fig, ax = plt.subplots()
        ax.add_artist(circle1)
        ax.add_artist(circle2)
        ax.add_artist(circle3)

        textstr1 = title2
        textstr2 = pattern_name
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(-0.75, 1.60, textstr1, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        ax.text(-0.75, -0.65, textstr2, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        ax.text(1.25, -0.45, textstr3, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)

        red_circle = mpatches.Patch(color='r', label=f'Total Data = {universe_members}')
        blue_circle = mpatches.Patch(color='blue', label=f'Class Size = {round(class2_percentage,2)}% of the total data')
        green_circle = mpatches.Patch(color='g', label=f'Pattern Support Size = {round(class2_support,2)}% of the class size')

        plt.legend(handles=[red_circle, blue_circle, green_circle], bbox_to_anchor=(1.75, 1.5))

        plt.axis('off')
        filename = f'Visualization//{featurename}//{class_short_name}//03_Features//{i}_ComplementaryClass.png'
        plt.ioff()
        plt.savefig(filename, bbox_inches='tight')

    # Visualizar patrones de 4 features
    for i in range(len(patt_list_4)):
        title1 = f'TARGET CLASS: {class_name}'
        pattern_name = f'Pattern: {file_contents[patt_list_4[i][0]:patt_list_4[i][1]]}'
        title2 = f'COMPLEMENT OF TARGET CLASS: {class_name}'

        raw_count = file_contents[count_list_4[i][0]:count_list_4[i][1]]
        count_list = ast.literal_eval(raw_count)
        
        raw_class_support = file_contents[tsupport_list_4[i][0]:tsupport_list_4[i][1]]
        class1_end = raw_class_support.find('%, ')
        class1_support = float(raw_class_support[1:class1_end])
        class2_end = raw_class_support.find('%]')
        class2_support = float(raw_class_support[class1_end+3:class2_end])
        
        try:
            class1_members = round(count_list[0]/(class1_support/100.0))
        except:
            class1_members = 0
        try:
            class2_members = round(count_list[1]/(class2_support/100.0))
        except:
            class2_members = 0

        universe_members = class1_members + class2_members
        class1_percentage = (class1_members / universe_members)*100
        class2_percentage = (class2_members / universe_members)*100
        universe_radius = 1.0

        class1_radius = math.sqrt(class1_members / universe_members)
        class2_radius = math.sqrt(class2_members / universe_members)
        try:
            pattern1_members = round(class1_members  * (class1_support/100.0))
        except:
            pattern1_members = 0
        try:
            pattern2_members = round(class2_members  * (class2_support/100.0))
        except:
            pattern2_members = 0

        pattern1_radius = math.sqrt(pattern1_members / universe_members)
        pattern2_radius = math.sqrt(pattern2_members / universe_members)


        # TARGET CLASS VISUALIZATION
        circle1 = plt.Circle((0.5, 0.5), universe_radius, color='r', clip_on=False)
        circle2 = plt.Circle((0.5, 0.5), class1_radius, color='blue', clip_on=False)
        circle3 = plt.Circle((0.5, 0.5), pattern1_radius, color='g', clip_on=False)

        fig, ax = plt.subplots()
        ax.add_artist(circle1)
        ax.add_artist(circle2)
        ax.add_artist(circle3)

        
        textstr1 = title1
        textstr2 = pattern_name
        textstr3 = f'Confidence: {file_contents[conf_list_4[i][0]:conf_list_4[i][1]]}\nDataset\'s Support: {file_contents[dsupport_list_4[i][0]:dsupport_list_4[i][1]]}'
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(-0.75, 1.60, textstr1, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        ax.text(-0.75, -0.65, textstr2, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        ax.text(1.25, -0.45, textstr3, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        

        red_circle = mpatches.Patch(color='r', label=f'Total Data = {universe_members}')
        blue_circle = mpatches.Patch(color='blue', label=f'Class Size = {round(class1_percentage,2)}% of the total data')
        green_circle = mpatches.Patch(color='g', label=f'Pattern Support Size = {round(class1_support,2)}% of the class size')

        plt.legend(handles=[red_circle, blue_circle, green_circle], bbox_to_anchor=(1.75, 1.5))

        plt.axis('off')
        filename = f'Visualization//{featurename}//{class_short_name}//04_Features//{i}_TargetClass.png'
        plt.ioff()
        plt.savefig(filename, bbox_inches='tight')
        
        # COMPLEMENT CLASS VISUALIZATION
        circle1 = plt.Circle((0.5, 0.5), universe_radius, color='r', clip_on=False)
        circle2 = plt.Circle((0.5, 0.5), class2_radius, color='blue', clip_on=False)
        circle3 = plt.Circle((0.5, 0.5), pattern2_radius, color='g', clip_on=False)

        fig, ax = plt.subplots()
        ax.add_artist(circle1)
        ax.add_artist(circle2)
        ax.add_artist(circle3)

        textstr1 = title2
        textstr2 = pattern_name
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(-0.75, 1.60, textstr1, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        ax.text(-0.75, -0.65, textstr2, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        ax.text(1.25, -0.45, textstr3, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)

        red_circle = mpatches.Patch(color='r', label=f'Total Data = {universe_members}')
        blue_circle = mpatches.Patch(color='blue', label=f'Class Size = {round(class2_percentage,2)}% of the total data')
        green_circle = mpatches.Patch(color='g', label=f'Pattern Support Size = {round(class2_support,2)}% of the class size')

        plt.legend(handles=[red_circle, blue_circle, green_circle], bbox_to_anchor=(1.75, 1.5))

        plt.axis('off')
        filename = f'Visualization//{featurename}//{class_short_name}//04_Features//{i}_ComplementaryClass.png'
        plt.ioff()
        plt.savefig(filename, bbox_inches='tight')
