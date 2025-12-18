'use client';

import { useState, useEffect, useMemo, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import Header from '@/components/Header';
import SettingsSidebar from '@/components/SettingsSidebar';
import { loadSettings } from '@/lib/settings';
import type { PhoneticTableData, PhoneticSyllable, Dialect, UserSettings } from '@/types';

// 聲母/韻母/聲調配置項類型
interface FilterOption {
  value: string;
  label: string;
  values?: string[]; // 變體聲母（如 s/x）
}

// 聲母配置
const INITIALS_SIYEN: FilterOption[] = [
  { value: 'b', label: 'b' },
  { value: 'p', label: 'p' },
  { value: 'm', label: 'm' },
  { value: 'f', label: 'f' },
  { value: 'v', label: 'v' },
  { value: 'd', label: 'd' },
  { value: 't', label: 't' },
  { value: 'n', label: 'n' },
  { value: 'l', label: 'l' },
  { value: 'g', label: 'g' },
  { value: 'k', label: 'k' },
  { value: 'ng', label: 'ng' },
  { value: 'h', label: 'h' },
  { value: 'z/j', label: 'z/j', values: ['z', 'j'] },
  { value: 'c/q', label: 'c/q', values: ['c', 'q'] },
  { value: 's/x', label: 's/x', values: ['s', 'x'] },
  { value: '', label: '零聲母' },
  { value: 'bb', label: '(bb)' },
  { value: 'gg', label: '(gg)' },
  { value: 'zz', label: '(zz)' },
];

const INITIALS_HAILIUK: FilterOption[] = [
  { value: 'b', label: 'b' },
  { value: 'p', label: 'p' },
  { value: 'm', label: 'm' },
  { value: 'f', label: 'f' },
  { value: 'v', label: 'v' },
  { value: 'd', label: 'd' },
  { value: 't', label: 't' },
  { value: 'n', label: 'n' },
  { value: 'l', label: 'l' },
  { value: 'g', label: 'g' },
  { value: 'k', label: 'k' },
  { value: 'ng', label: 'ng' },
  { value: 'h', label: 'h' },
  { value: 'z', label: 'z' },
  { value: 'c', label: 'c' },
  { value: 's', label: 's' },
  { value: 'zh', label: 'zh' },
  { value: 'ch', label: 'ch' },
  { value: 'sh', label: 'sh' },
  { value: 'rh', label: 'rh' },
  { value: '', label: '零聲母' },
  { value: 'bb', label: '(bb)' },
  { value: 'gg', label: '(gg)' },
  { value: 'zz', label: '(zz)' },
];

// 聲調配置
const TONES_SIYEN: FilterOption[] = [
  { value: '1', label: '1 (陰平)' },
  { value: '2', label: '2 (上聲)' },
  { value: '3', label: '3 (去聲)' },
  { value: '4', label: '4 (陰入)' },
  { value: '5', label: '5 (陽平)' },
  { value: '8', label: '8 (陽入)' },
];

const TONES_HAILIUK: FilterOption[] = [
  { value: '1', label: '1 (陰平)' },
  { value: '2', label: '2 (上聲)' },
  { value: '3', label: '3 (陰去)' },
  { value: '4', label: '4 (陰入)' },
  { value: '5', label: '5 (陽平)' },
  { value: '7', label: '7 (陽去)' },
  { value: '8', label: '8 (陽入)' },
];

function PhoneticTableContent() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const [data, setData] = useState<PhoneticTableData | null>(null);
  const [loading, setLoading] = useState(true);
  const [dialect, setDialect] = useState<Dialect>('siyen');

  // 為四縣和海陸分別存儲選擇狀態（記憶功能）
  const [filters, setFilters] = useState<{
    siyen: { initials: Set<string>; rhymes: Set<string>; tones: Set<string> };
    hailiuk: { initials: Set<string>; rhymes: Set<string>; tones: Set<string> };
  }>({
    siyen: { initials: new Set(), rhymes: new Set(), tones: new Set() },
    hailiuk: { initials: new Set(), rhymes: new Set(), tones: new Set() }
  });

  const [showPronunciations, setShowPronunciations] = useState(true);
  const [settings, setSettings] = useState<UserSettings | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // 當前腔調的選擇狀態
  const selectedInitials = filters[dialect].initials;
  const selectedRhymes = filters[dialect].rhymes;
  const selectedTones = filters[dialect].tones;

  // 載入資料和設定
  useEffect(() => {
    const loadedSettings = loadSettings();
    setSettings(loadedSettings);

    fetch('/phonetic-table.json')
      .then(res => res.json())
      .then((jsonData: PhoneticTableData) => {
        setData(jsonData);
        setLoading(false);
      })
      .catch(err => {
        console.error('載入同音字表失敗:', err);
        setLoading(false);
      });
  }, []);

  // 從 URL 讀取參數
  useEffect(() => {
    if (!data) return;

    const dialectParam = searchParams.get('dialect');
    if (dialectParam === 'siyen' || dialectParam === 'hailiuk') {
      setDialect(dialectParam);
    }

    // 從音節參數自動解析（來自條目頁面跳轉）
    const syllableParam = searchParams.get('syllable');
    if (syllableParam) {
      const currentDialect = dialectParam === 'hailiuk' ? 'hailiuk' : 'siyen';
      const syllable = data[currentDialect].syllables.find(s => s.p.numbered === syllableParam);
      if (syllable) {
        // 對於四縣話的變體聲母（s/x, z/j, c/q），需要同時選中兩個
        const initialSet = new Set<string>();
        const initial = syllable.i;

        if (currentDialect === 'siyen') {
          if (initial === 's' || initial === 'x') {
            initialSet.add('s');
            initialSet.add('x');
          } else if (initial === 'z' || initial === 'j') {
            initialSet.add('z');
            initialSet.add('j');
          } else if (initial === 'c' || initial === 'q') {
            initialSet.add('c');
            initialSet.add('q');
          } else {
            initialSet.add(initial);
          }
        } else {
          initialSet.add(initial);
        }

        setFilters(prev => ({
          ...prev,
          [currentDialect]: {
            initials: initialSet,
            rhymes: new Set([syllable.r]),
            tones: new Set([syllable.t])
          }
        }));
        return;
      }
    }

    const initialsParam = searchParams.get('i');
    const rhymesParam = searchParams.get('r');
    const tonesParam = searchParams.get('t');

    if (initialsParam || rhymesParam || tonesParam) {
      const currentDialect = dialectParam === 'hailiuk' ? 'hailiuk' : 'siyen';
      setFilters(prev => ({
        ...prev,
        [currentDialect]: {
          initials: initialsParam ? new Set(initialsParam.split(',')) : prev[currentDialect].initials,
          rhymes: rhymesParam ? new Set(rhymesParam.split(',')) : prev[currentDialect].rhymes,
          tones: tonesParam ? new Set(tonesParam.split(',')) : prev[currentDialect].tones
        }
      }));
    }
  }, [searchParams, data]);

  // 更新 URL
  const updateURL = () => {
    const params = new URLSearchParams();
    params.set('dialect', dialect);

    if (selectedInitials.size > 0) {
      params.set('i', Array.from(selectedInitials).join(','));
    }
    if (selectedRhymes.size > 0) {
      params.set('r', Array.from(selectedRhymes).join(','));
    }
    if (selectedTones.size > 0) {
      params.set('t', Array.from(selectedTones).join(','));
    }

    router.replace(`/phonetic-table?${params.toString()}`, { scroll: false });
  };

  // 獲取當前方言的配置
  const initials = dialect === 'siyen' ? INITIALS_SIYEN : INITIALS_HAILIUK;
  const tones = dialect === 'siyen' ? TONES_SIYEN : TONES_HAILIUK;

  // 從資料中提取所有韻母（按字母順序）
  const allRhymes = useMemo(() => {
    if (!data) return [];
    const rhymes = new Set<string>();
    data[dialect].syllables.forEach(s => rhymes.add(s.r));
    return Array.from(rhymes).sort();
  }, [data, dialect]);

  // 過濾音節
  const filteredSyllables = useMemo(() => {
    if (!data) return [];

    // 如果全都沒選擇，返回空陣列（不顯示）
    if (selectedInitials.size === 0 && selectedRhymes.size === 0 && selectedTones.size === 0) {
      return [];
    }

    const syllables = data[dialect].syllables;

    return syllables.filter(s => {
      const matchInitial = selectedInitials.size === 0 || selectedInitials.has(s.i);
      const matchRhyme = selectedRhymes.size === 0 || selectedRhymes.has(s.r);
      const matchTone = selectedTones.size === 0 || selectedTones.has(s.t);
      return matchInitial && matchRhyme && matchTone;
    });
  }, [data, dialect, selectedInitials, selectedRhymes, selectedTones]);

  // 切換選擇
  const toggleInitial = (value: string | string[]) => {
    const values = Array.isArray(value) ? value : [value];
    const newSet = new Set(selectedInitials);

    // 檢查是否所有值都已選中
    const allSelected = values.every(v => newSet.has(v));

    if (allSelected) {
      // 取消選擇
      values.forEach(v => newSet.delete(v));
    } else {
      // 添加選擇
      values.forEach(v => newSet.add(v));
    }

    setFilters(prev => ({
      ...prev,
      [dialect]: { ...prev[dialect], initials: newSet }
    }));
  };

  const toggleRhyme = (value: string) => {
    const newSet = new Set(selectedRhymes);
    if (newSet.has(value)) {
      newSet.delete(value);
    } else {
      newSet.add(value);
    }
    setFilters(prev => ({
      ...prev,
      [dialect]: { ...prev[dialect], rhymes: newSet }
    }));
  };

  const toggleTone = (value: string) => {
    const newSet = new Set(selectedTones);
    if (newSet.has(value)) {
      newSet.delete(value);
    } else {
      newSet.add(value);
    }
    setFilters(prev => ({
      ...prev,
      [dialect]: { ...prev[dialect], tones: newSet }
    }));
  };

  // 切換方言（不清除選擇，實現記憶功能）
  const handleDialectChange = (newDialect: Dialect) => {
    setDialect(newDialect);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="text-gray-600 dark:text-gray-300">載入中...</div>
      </div>
    );
  }

  if (!data || !settings) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="text-red-600 dark:text-red-400">載入失敗</div>
      </div>
    );
  }

  const handleSettingsChange = (newSettings: UserSettings) => {
    setSettings(newSettings);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header onSettingsClick={() => setSidebarOpen(true)} />

      <main className="container mx-auto px-4 py-8 max-w-6xl">
        <h1 className="text-3xl font-bold text-gray-800 dark:text-gray-100 mb-6">同音字表</h1>

        {/* 方言切換 */}
        <div className="mb-6 flex items-center space-x-4">
          <span className="text-gray-700 dark:text-gray-300 font-medium">方言：</span>
          <button
            onClick={() => handleDialectChange('siyen')}
            className={`px-6 py-2 rounded-lg font-medium transition-colors ${
              dialect === 'siyen'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
            }`}
          >
            四縣話
          </button>
          <button
            onClick={() => handleDialectChange('hailiuk')}
            className={`px-6 py-2 rounded-lg font-medium transition-colors ${
              dialect === 'hailiuk'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
            }`}
          >
            海陸話
          </button>
        </div>

        {/* 聲母選擇 */}
        <div className="mb-6 bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm">
          <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-3">聲母</h2>
          <div className="flex flex-wrap gap-2">
            {initials.map(initial => {
              const values = initial.values || [initial.value];
              const isSelected = values.every(v => selectedInitials.has(v));
              return (
                <button
                  key={initial.value}
                  onClick={() => toggleInitial(values)}
                  className={`px-3 py-1.5 rounded font-medium transition-colors ${
                    isSelected
                      ? 'bg-blue-500 dark:bg-blue-600 text-white'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                  }`}
                >
                  {initial.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* 韻母選擇 */}
        <div className="mb-6 bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm">
          <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-3">韻母</h2>
          <div className="flex flex-wrap gap-2">
            {allRhymes.map(rhyme => {
              const isSelected = selectedRhymes.has(rhyme);
              return (
                <button
                  key={rhyme}
                  onClick={() => toggleRhyme(rhyme)}
                  className={`px-3 py-1.5 rounded font-medium transition-colors ${
                    isSelected
                      ? 'bg-green-500 dark:bg-green-600 text-white'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                  }`}
                >
                  {rhyme}
                </button>
              );
            })}
          </div>
        </div>

        {/* 聲調選擇 */}
        <div className="mb-6 bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm">
          <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-3">聲調</h2>
          <div className="flex flex-wrap gap-2">
            {tones.map(tone => {
              const isSelected = selectedTones.has(tone.value);
              return (
                <button
                  key={tone.value}
                  onClick={() => toggleTone(tone.value)}
                  className={`px-3 py-1.5 rounded font-medium transition-colors ${
                    isSelected
                      ? 'bg-orange-500 dark:bg-orange-600 text-white'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                  }`}
                >
                  {tone.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* 顯示/隱藏拼音方案開關 */}
        <div className="mb-6 flex items-center space-x-3">
          <label className="flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={showPronunciations}
              onChange={(e) => setShowPronunciations(e.target.checked)}
              className="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
            />
            <span className="ml-2 text-gray-700 dark:text-gray-300">顯示其他羅馬字方案</span>
          </label>
        </div>

        {/* 結果顯示 */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-100 mb-4">
            結果（共 {filteredSyllables.length} 個音節）
          </h2>

          {filteredSyllables.length === 0 ? (
            <p className="text-gray-600 dark:text-gray-400">請選擇聲母、韻母或聲調以顯示結果</p>
          ) : (
            <div className="space-y-6">
              {filteredSyllables.map((syllable, idx) => (
                <div key={idx} className="border-b border-gray-200 dark:border-gray-700 pb-6 last:border-b-0">
                  {/* 音節拼音（帶顏色） */}
                  <h3 className="text-2xl font-bold mb-2">
                    {syllable.i && <span className="text-blue-600 dark:text-blue-400">{syllable.i}</span>}
                    <span className="text-green-600 dark:text-green-400">{syllable.r}</span>
                    <sup className="text-orange-600 dark:text-orange-400">{syllable.t}</sup>
                  </h3>

                  {/* 其他拼音方案 */}
                  {showPronunciations && (
                    <div className="text-sm text-gray-600 dark:text-gray-400 mb-3 space-x-3">
                      <span>客拼數字：{syllable.p.numbered}</span>
                      <span>|</span>
                      <span>客拼符號：{syllable.p.marked}</span>
                      {syllable.p.pfs && (
                        <>
                          <span>|</span>
                          <span>白話字：{
                            // bb, gg, zz 聲母在白話字中無對應，顯示 -
                            (syllable.i === 'bb' || syllable.i === 'gg' || syllable.i === 'zz')
                              ? '-'
                              : syllable.p.pfs
                          }</span>
                        </>
                      )}
                      <span>|</span>
                      <span>原書方案：{syllable.p.original}</span>
                      {syllable.p.ipa && (
                        <>
                          <span>|</span>
                          <span>國際音標：/{syllable.p.ipa}/</span>
                        </>
                      )}
                    </div>
                  )}

                  {/* 字列表 */}
                  <div className="flex flex-wrap gap-2 text-2xl text-gray-900 dark:text-gray-100">
                    {syllable.c.length === 0 ? (
                      <span className="text-gray-500 dark:text-gray-400 text-base">(無對應漢字)</span>
                    ) : (
                      syllable.c.map((charObj, charIdx) => (
                        charObj.id ? (
                          <Link
                            key={charIdx}
                            href={`/word/${dialect}/${charObj.id}`}
                            className={`hover:bg-gray-100 dark:hover:bg-gray-700 px-2 py-1 rounded transition-colors border-b-2 ${
                              charObj.m
                                ? 'border-dashed border-gray-400 dark:border-gray-500'
                                : 'border-solid border-gray-300 dark:border-gray-600'
                            }`}
                            title={charObj.m ? '有多個條目或多個讀音' : ''}
                          >
                            {charObj.char}
                          </Link>
                        ) : (
                          <span
                            key={charIdx}
                            className={`px-2 py-1 border-b-2 ${
                              charObj.m
                                ? 'border-dashed border-gray-400 dark:border-gray-500'
                                : 'border-solid border-gray-300 dark:border-gray-600'
                            }`}
                            title={charObj.m ? '有多個條目或多個讀音' : ''}
                          >
                            {charObj.char}
                          </span>
                        )
                      ))
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      <SettingsSidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        settings={settings}
        onSettingsChange={handleSettingsChange}
      />
    </div>
  );
}

export default function PhoneticTablePage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="text-gray-600 dark:text-gray-300">載入中...</div>
      </div>
    }>
      <PhoneticTableContent />
    </Suspense>
  );
}
