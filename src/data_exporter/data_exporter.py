import matplotlib.pyplot as plt
from matplotlib import ticker
import pandas as pd
import os


def get_excel_vol(input_data,
                  moneyness_axis,
                  svi_model,
                  commodity_code,
                  file_path,
                  code_that_we_want):
    days_to_maturity = input_data.days_to_maturity()
    t_axis_value = 0
    for i in range(100):
        t_axis_value = t_axis_value + 7
        if t_axis_value >= days_to_maturity[0]:
            break

    t_axis_new = [t_axis_value]
    for i in range(100):
        t_axis_value = t_axis_value + 7
        if t_axis_value > days_to_maturity[-1]:
            break
        t_axis_new.append(t_axis_value)

    index_name = []
    for i in range(len(t_axis_new)):
        index_content = str(int(t_axis_new[i] / 7))+'W'
        index_name.append(index_content)

    columns_name = []
    for i in range(len(moneyness_axis)):
        columns_content = str(round(moneyness_axis[i] * 100)) + '%'
        columns_name.append(columns_content)

    vol = pd.DataFrame(index=index_name, columns=columns_name)
    for i in range(len(t_axis_new)):
        for j in range(len(moneyness_axis)):
            vol[columns_name[j]][index_name[i]] = svi_model.vol(t_axis_new[i]/365.0, moneyness_axis[j])

    vol.to_excel(file_path + '/' + 'IVSurface-' + commodity_code + '.xlsx', sheet_name='波动率标准模版')
    vol = pd.read_excel(file_path + '/' + 'IVSurface-' + commodity_code + '.xlsx')
    continuous_commodity_code = code_that_we_want
    vol1 = vol.rename(columns={'Unnamed: 0': continuous_commodity_code})
    vol1.to_excel(file_path + '/' + 'IVSurface-' + commodity_code + '.xlsx', index=False, sheet_name='波动率标准模版')


def get_fitting_performance(option_type,
                            input_data,
                            svi_model,
                            moneyness_axis,
                            valuation_date,
                            commodity_code,
                            file_path):
    t_axis = input_data.ttms()
    days_to_maturity = input_data.days_to_maturity()
    file_path = file_path + 'picture/' + commodity_code + '\\'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    for i in range(len(t_axis)):
        plt.figure(figsize=(7, 5))
        moneyness = svi_model.moneyness[i]
        iv = svi_model.implied_vols[i]
        plt.scatter(moneyness, iv, s=5)
        plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=2))
        plt.gca().xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        fitting_iv = svi_model.vol(t_axis[i], moneyness_axis)
        plt.plot(moneyness_axis,
                 fitting_iv,
                 label=str(int(days_to_maturity[i])) + ' days to maturity')
        plt.xlabel('Moneyness(K/$F_T$)', fontsize=8)
        plt.ylabel('Implied Volatility(' + r'$\sigma$' + ')', fontsize=8)
        if option_type == 'C':
            plt.title(commodity_code + '-Call-Option\n' + str(valuation_date), fontsize=8)
        elif option_type == 'P':
            plt.title(commodity_code + '-Put-Option\n' + str(valuation_date), fontsize=8)
        plt.legend(loc='best', frameon=False)
        plt.tight_layout()
        plt.savefig(file_path + '/' + commodity_code + '-{}.png'.format(int(days_to_maturity[i])))
        plt.clf()
        plt.close()


def get_variance_plot(option_type,
                      input_data,
                      svi_model,
                      moneyness_axis,
                      valuation_date,
                      commodity_code,
                      file_path):
    t_axis = input_data.ttms()
    days_to_maturity = input_data.days_to_maturity()
    plt.figure(figsize=(7, 5))
    plt.rcParams.update({'font.size': 20})
    plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=2))
    plt.gca().xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    for i in range(len(t_axis)):
        fitting_var = svi_model.total_var(t_axis[i], moneyness_axis)
        plt.plot(moneyness_axis,
                 fitting_var,
                 label=str(int(days_to_maturity[i])))
    plt.xlabel('Moneyness(K/$F_T$)', fontsize=8)
    plt.ylabel('Implied Total Variance('r'$\sigma$''$^2$T)', fontsize=8)
    if option_type == 'C':
        plt.title(commodity_code + '-Call-Option\n' + str(valuation_date), fontsize=8)
    elif option_type == 'P':
        plt.title(commodity_code + '-Put-Option\n' + str(valuation_date), fontsize=8)
    plt.legend(loc='center left',
               bbox_to_anchor=(1, 0.5),
               title='days to maturity',
               fontsize=8,
               title_fontsize=8)
    plt.tight_layout()
    file_path = file_path + 'picture/' + commodity_code + '\\'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    plt.savefig(file_path + '/' + commodity_code + 'Surface.png')
    plt.clf()
    plt.close()
